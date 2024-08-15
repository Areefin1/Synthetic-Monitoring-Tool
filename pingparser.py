import pingparsing
from datetime import datetime
import time
import socket
from yamlreader import main as read_yaml

'''
Main function to call yamlreader.py file's main function that asks the user for YAML file to parse.
It parses multiple destinations with a specified time interval and number of ping requests or probes for each destination.
Finally, it executes process_ping() function to start pinging each destination and gather information and calls the simplified_stats() function to 
print the simplified and readable ping statistics output.
'''
def main():

    config = read_yaml()

    if config is None or 'destinations' not in config:
        print("Error: Missing required key or file information in the YAML file.")
        return
    
    interval = check_value(config['interval'])
    
    for item in config['destinations']:
        if 'destination' not in item or 'count' not in item:
            print(f"Error: Missing required {item} in the YAML file. Proceeding to next destination.")
            continue
    
        destination = check_destination(item['destination'].strip())
        count = check_value(item['count'])

        if destination and count:
            results = process_ping(destination, count, interval)
            simplified_stats(results)

'''
Pings each server's "destination" "count" number of times at a specified time "interval" in seconds in between each destination.

 Args:
        destination (str): Website or IP address.
        count (int): Number of ping requests or probes.
        interval (int): Time interval in seconds.
Returns:
        stats (dict): Contains all aggregated ping information and statistics.
'''
def process_ping(destination, count, interval):

    # Intialization
    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination = destination
    transmitter.count = count

    startTime = datetime.now()
    time.sleep(interval)
    result = transmitter.ping()
    endTime = datetime.now()

    stats = ping_parser.parse(result).as_dict()

    raw_output = result.stdout.strip()
    icmp_replies = raw_output.split("\n")
    print()

    # Print each ICMP reply message
    for icmp_reply in icmp_replies:
        if 'Reply from' in icmp_reply or 'Pinging' in icmp_reply:
            print(icmp_reply.strip().replace("TTL", "Time-to-Live"))

    print()

    # Calculate elapsed time using the start and end timestamps.
    elapsedTime = endTime - startTime
    total_seconds = elapsedTime.total_seconds() 
    formatted_elapsedTime = f"{int(total_seconds // 3600):02}:{int((total_seconds % 3600) // 60):02}:{total_seconds % 60:06.3f}"

    stats['start_time'] = startTime.strftime('%m/%d/%y %H:%M:%S')
    stats['end_time'] = endTime.strftime('%m/%d/%y %H:%M:%S')
    stats['elapsed_time'] = formatted_elapsedTime

    return stats

'''
Prints a more simplified and readable ping statistic output.

 Args:
        result (dict): Dictionary containing parsed ping information.
Returns:
        None
'''
def simplified_stats(result):

    print('Simplified Ping Statistics:\n')
    print(f'Ping destination: {result.get("destination")}')
    print(f"Date and time when the ping request was first initiated/sent: {result.get('start_time')}")
    print(f'Number of packets sent: {result.get("packet_transmit")}')
    print(f'Number of packets received: {result.get("packet_receive")}')
    print(f'Number of packets lost: {result.get("packet_loss_count")}')
    print(f'Packet loss in percentage: {result.get("packet_loss_rate")}%')
    print(f'Fastest round-trip time in milliseconds: {result.get("rtt_min")} ms')
    print(f'Slowest round-trip time in milliseconds: {result.get("rtt_max")} ms')
    print(f'Average round-trip time in milliseconds: {result.get("rtt_avg")} ms')
    print(f"Date and time when final ping request was received: {result.get('end_time')}")
    print(f"Time elapsed: {result.get('elapsed_time')}\n")

'''
Check and validate config file's input for transmitter.count and time interval value with exception handling.
'''
def check_value(value):

    try:
        if value <= 0:
            print("Error: The input value must be a positive integer.")
            return None
        else:
            return value 
    except ValueError:
        print("Error: Invalid input. Please ensure that the config contains valid positive integer values for count and interval and try again.")
        return None
    except Exception as e:
        print(f"An unexpected error has occurred: {e}")
        return None

'''
Check and validate config file's input value for destination with exception handling.
'''
def check_destination(destination):

    try:
        if not destination:
            raise ValueError("The destination address cannot be empty. Please ensure that the config contains valid hostname or IP address and try again.")
        socket.gethostbyname(destination)
        return destination 
    except ValueError as e:
        print(f"Error: {e}")
        return None
    except socket.gaierror:
        print(f"Error: Invalid destination. Either '{destination}' does not exist or mistyped. Please ensure that the config contains valid hostname or IP address and try again.")
        return None
    except Exception as e:
        print(f"An unexpected error has occurred: {e}")
        return None
    
# Execute main directly and not when imported in a different file.
if __name__ == "__main__":
    
    main()