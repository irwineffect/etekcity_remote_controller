extern crate serialport;
extern crate bufstream;
use std::io::BufRead;
use std::io::Write;
use std::net;
use std::thread;
use std::time::Duration;

// use rumqttc::Incoming;
// use rumqttc::Publish;

extern crate rumqttc;

fn mqtt_advertise(mqtt_client: &mut rumqttc::Client, channel: usize, id: &str) {
    let discovery_msg = format!(r#"
    {{
        "name": "{id}",
        "unique_id": "{id}",
        "device_class": "switch",
        "command_topic": "etekcityd/{channel}"
    }}
    "#);
    mqtt_client.subscribe(format!("etekcityd/{channel}"), rumqttc::QoS::AtMostOnce).unwrap();
    mqtt_client.publish(format!("homeassistant/switch/{channel}/config"), rumqttc::QoS::AtMostOnce, true, discovery_msg).unwrap();

}

const CHANNEL_CODES: [&[u8]; 4] = [ 
                              "010011".as_bytes(),
                              "011100".as_bytes(),
                              "110000".as_bytes(),
                              "010000".as_bytes(),
                            //   "010000".as_bytes()
                            ];

fn control_channel(s: &mut impl Write, channel: usize, state: usize) {
    let prefix = "01000101010101".as_bytes();
    let suffix = "0\0".as_bytes();

    
    let on_off_codes = vec![ "1100".as_bytes(),
                             "0011".as_bytes()
                           ];

    s.write(prefix).unwrap();
    s.write(CHANNEL_CODES[channel-1]).unwrap();
    s.write(on_off_codes[state]).unwrap();
    s.write(suffix).unwrap();
    s.flush().unwrap();
}

fn main() {
    //println!("ports: {:?}", serialport::posix::available_ports());
    let mut s = match serialport::open("/dev/light_controller")
    {
        Ok(t) => t,
        Err(e) => panic!("failed opening port: {}", e)

    };

    s.write_data_terminal_ready(true).unwrap();
    std::thread::sleep(std::time::Duration::new(1,0));
    s.write_data_terminal_ready(false).unwrap();

    let mut s = bufstream::BufStream::new(s);

    println!("waiting for arduino to boot.");
    loop
    {
        let mut linebuf: String = String::new();
        match s.read_line(&mut linebuf)
        {
            Ok(_) =>
            {
                if linebuf.contains("initialized")
                {
                    break;
                }
            }
            Err(e) => match e.kind()
            {
                std::io::ErrorKind::TimedOut =>
                {
                    std::thread::sleep(std::time::Duration::new(1,0));
                },
                _ => panic!("{:#?}", e)
            }

        }
    }
    println!("arduino booted!");

    /*
    let off_code = "1100".as_bytes();
    let on_code  = "0011".as_bytes();
    let channel_code = "011100".as_bytes();



    s.write(preamble);
    s.write(channel_code);
    s.write(on_code);
    s.write("0".as_bytes());
    s.write(&[0x00u8]);
    s.flush();
    */

    

    let socket = match net::UdpSocket::bind("0.0.0.0:1666")
    {
        Ok(s) => s,
        Err(e) => panic!("{}", e)
    };
    socket.set_nonblocking(true).unwrap();

    let (mut mqtt_client, mut mqtt_connection) = {
        let options = rumqttc::MqttOptions::new("etekcityd", "telperion.lan", 1883);
        rumqttc::Client::new(options, 10)
    };

    mqtt_advertise(&mut mqtt_client, 1, "Den Fan");
    mqtt_advertise(&mut mqtt_client, 3, "Garage Lights");
    mqtt_advertise(&mut mqtt_client, 4, "Living Room Lights");


    let mut udp_buf: [u8; 2] = [0; 2];

    println!("starting main loop");
    loop {

        // Look for a MQTT message
        match mqtt_connection.recv_timeout(Duration::from_millis(50)) {
            Ok(Ok(rumqttc::Event::Incoming( rumqttc::mqttbytes::v4::Packet::Publish(msg)))) => {
                let channel: usize = msg.topic.split("/").last().and_then(|s| s.parse().ok()).unwrap();
                let state = if msg.payload  == "ON" {
                    true
                } else if msg.payload  == "OFF"  {
                    false
                }
                else {
                    println!("unexpected mqtt payload: {:?}", msg.payload);
                    continue;
                };

                control_channel(&mut s, channel, state.into());
                    
            }
            // Ok(Innotification) => {
            // }
            Err(rumqttc::RecvTimeoutError::Timeout) => {
                // Timeout is ok
            }
            Ok(Err(e)) => {
                dbg!(e);
            }
            Err(e) => {
                dbg!(e);
            }
            _ => {
                // Don't care
            }
        }

        // Check UDP port
        match socket.recv_from(&mut udp_buf)
        {
            Ok((_, src)) =>
            {
                let channel: usize = udp_buf[0] as usize;
                let state: usize = udp_buf[1] as usize;


                if channel < 1 || channel > CHANNEL_CODES.len()
                {
                    println!("invalid channel");
                    println!("received {:#?} from {}: ", udp_buf, src);
                    continue;
                }
                if state > 1
                {
                    println!("invalid state");
                    println!("received {:#?} from {}: ", udp_buf, src);
                    continue;
                }

                println!("setting channel {} to {}", channel, state);

                control_channel(&mut s, channel, state);

              
            }
            Err(ref e) if e.kind() == std::io::ErrorKind::WouldBlock => {
            }
            Err(e) => panic!("{}", e)
        }

        thread::sleep(Duration::from_millis(50))
    }
}
