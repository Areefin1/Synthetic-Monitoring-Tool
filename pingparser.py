import pingparsing
from datetime import datetime
import socket

'''
Main function to prompt the user for destination server and number of ping requests, execute ping commands, print its contents in simplified view.
Repeats until valid input is provided for both destination and number of ping requestas.
'''
def main():

    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()

    # Prompt user for valid destination and number of ping requests.
    transmitter.destination = check_destination("Enter destination: ")
    transmitter.count = check_value("Enter the number of ping request: ")
            
    print()

    # Record the timestamps when the first and last ping commands are sent and received.
    startTime = datetime.now()
    result = transmitter.ping()
    endTime = datetime.now()

    # Extract and display relevant information from the raw output.
    raw_output = result.stdout
    icmp_replies = raw_output.split("\n")

    for icmp_reply in icmp_replies:
        if "Reply from" in icmp_reply or "Pinging" in icmp_reply:
            print(icmp_reply.strip().replace("TTL", "Time-To-Live"))

    print()

    simplified_stats(ping_parser.parse(result).as_dict(), startTime, endTime)


'''
Prints a more simplified and readable ping statistic output.

 Args:
        result (dict): Dictionary containing parsed ping information.
        start (datetime): Timestamp when the ping request was initiated.
        end (datetime): Timestamp when the final ping response was received.

Returns:
        None
'''
def simplified_stats(result, start, end):
    
    # Calculate elapsed time using the start and end timestamps.
    elapsedTime = end - start
    total_seconds = elapsedTime.total_seconds() 
    formatted_elapsedTime = f"{int(total_seconds // 3600):02}:{int((total_seconds % 3600) // 60):02}:{total_seconds % 60:06.3f}"

    print('Simplified Ping Statistics: ')
    print(f'Ping destination: {result.get("destination")}')
    print(f"Date and time when the ping request was first initiated/sent: {start.strftime('%m/%d/%y %H:%M:%S')}")
    print(f'Number of packets sent: {result.get("packet_transmit")}')
    print(f'Number of packets received: {result.get("packet_receive")}')
    print(f'Number of packets lost: {result.get("packet_loss_count")}')
    print(f'Packet loss in percentage: {result.get("packet_loss_rate")}%')
    print(f'Fastest round-trip time in milliseconds: {result.get("rtt_min")} ms')
    print(f'Slowest round-trip time in milliseconds: {result.get("rtt_max")} ms')
    print(f'Average round-trip time in milliseconds: {result.get("rtt_avg")} ms')
    print(f"Date and time when final ping request was received: {end.strftime('%m/%d/%y %H:%M:%S')}")
    print(f'Time elapsed: {formatted_elapsedTime}')

'''
Check and validate user's input for transmitter.count value with exception handling.
'''
def check_value(prompt):

    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Error: The number of ping request must be greater than zero.")
            else:
                return value 
        except ValueError:
            print("Error: Invalid input. Please enter a positive integer.")
        except Exception as e:
            print(f"An unexpected error has occurred: {e}")
            break

'''
Check and validate user's input for destination value with exception handling.
'''
def check_destination(prompt):

    while True:
        try:
            destination = input(prompt).strip()
            if not destination:
                raise ValueError("The destination address cannot be empty. Please enter a valid hostname or IP address.")
            socket.gethostbyname(destination)
            return destination 
        except ValueError as e:
            print(f"Error: {e}")
        except socket.gaierror:
            print(f"Error: Invalid destination. Either '{destination}' does not exist or mistyped. Please enter a valid hostname or IP address and try again.")
        except Exception as e:
            print(f"An unexpected error has occurred: {e}")
            break
    
# Execute main directly and not when imported in a different file.
if __name__ == "__main__":
    
    main()