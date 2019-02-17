extern crate serialport;
extern crate bufstream;
use std::io::BufRead;
use std::io::Write;
use std::net;

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

    let prefix = "01000101010101".as_bytes();
    let suffix = "0\0".as_bytes();

    let channel_codes = vec![ "010011".as_bytes(),
                              "011100".as_bytes(),
                              "110000".as_bytes(),
                              "010000".as_bytes(),
                              "010000".as_bytes()
                            ];

    let on_off_codes = vec![ "1100".as_bytes(),
                             "0011".as_bytes()
                           ];

    let socket = match net::UdpSocket::bind("0.0.0.0:1666")
    {
        Ok(s) => s,
        Err(e) => panic!(e)
    };

    let mut udp_buf: [u8; 2] = [0; 2];

    loop
    {
        match socket.recv_from(&mut udp_buf)
        {
            Ok((_, src)) =>
            {
                let channel: usize = udp_buf[0] as usize;
                let state: usize = udp_buf[1] as usize;

                if channel < 1 || channel > channel_codes.len()
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

                s.write(prefix).unwrap();
                s.write(channel_codes[channel-1]).unwrap();
                s.write(on_off_codes[state]).unwrap();
                s.write(suffix).unwrap();
                s.flush().unwrap();
            }
            Err(e) => panic!(e)
        }
    }
}
