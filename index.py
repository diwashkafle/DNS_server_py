import time
import socket

def make_dns_response(data):
    start_time = time.time()  # Start timing the response creation
    transaction_id = data[:2]  # First two bytes of the request
    flags = b'\x81\x80'  # Standard query response, no error
    questions = data[4:6]  # Number of questions
    answer_rrs = b'\x00\x01'  # One answer
    authority_rrs = b'\x00\x00'  # No authority records
    additional_rrs = b'\x00\x00'  # No additional records
    question_part = data[12:]  # The question part from the request

    # Domain parsing is here for debugging purposes
    domain_parts = []
    x = 12
    y = data[x]
    while y != 0:
        domain_parts.append(data[x+1:x+y+1].decode())
        x += y + 1
        y = data[x]

    domain = '.'.join(domain_parts)
    print(f"Requested domain: {domain}")

    # Constructing the response
    answer_part = (question_part +
                   b'\xc0\x0c' +  # Pointer to domain name
                   b'\x00\x01' +  # Type A
                   b'\x00\x01' +  # Class IN
                   b'\x00\x00\x00\x3c' +  # TTL (60 seconds)
                   b'\x00\x04' +  # Data length
                   socket.inet_aton('93.184.216.34'))  # IP address

    response = (transaction_id + flags + questions + answer_rrs +
                authority_rrs + additional_rrs + question_part + answer_part)
    
    end_time = time.time()
    print(f"DNS response created in {end_time - start_time:.4f} seconds")
    return response

def run_dns_server(port=55000):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('127.0.0.1', port))
        print(f"DNS Server is up and listening on port {port}")

        while True:
            print("We are inside while loop!")
            try:
                print("Waiting for DNS request...")
                recv_start_time = time.time()
                print(recv_start_time)
                data, addr = sock.recvfrom(512)
                print('it is after sever recevies the request!!')
                print(f"Raw DNS query data: {data.hex()}")
                recv_end_time = time.time()
                print(f"Received DNS request from {addr} in {recv_end_time - recv_start_time:.4f} seconds")

                process_start_time = time.time()
                response = make_dns_response(data)
                process_end_time = time.time()
                print(f"Processed DNS request in {process_end_time - process_start_time:.4f} seconds")

                send_start_time = time.time()
                sock.sendto(response, addr)
                send_end_time = time.time()
                print(f"Sent response to {addr} in {send_end_time - send_start_time:.4f} seconds")

            except Exception as e:
                print(f"Error: {e}", flush=True)

# Main block to call the function
if __name__ == "__main__":
    run_dns_server()