import pingparsing
from datetime import datetime
import time
import socket
from yamlreader import main as read_yaml

'''
Main function to call yamlreader.py file's main function that asks the user for YAML file to parse.
It accepts and parses multiple destinations and it assigns each values for each respective destination, number of ping requests or probes, and 
time interval in seconds.
Finally, it executes process_ping() function to start pinging each destination and gather information and calls the simplified_stats() function to 
print the simplified and readable ping statistics output.
'''
def main():

    config = read_yaml()

    if config is None or 'destinations' not in config:
        print("Error: Missing required key or file information in the YAML file.")
        return
    
    for item in config['destinations']:
        if 'destination' not in item or 'count' not in item or 'interval' not in item:
            print(f"Error: Missing required {item} in the YAML file. Proceeding to next destination.")
            continue
    
        destination = check_destination(item['destination'].strip())
        count = check_value(item['count'])
        interval = check_value(item['interval'])

        if destination and count and interval:
            results = process_ping(destination, count, interval)
            simplified_stats(results)

'''
Pings server's "destination" "count" number of times after every time "interval" in seconds.

 Args:
        destination (str): Website or IP address.
        count (int): Number of ping requests or probes.
        interval (int): Time interval in seconds.
Returns:
        results (dict): Contains all aggregated ping information and statistics.
'''
def process_ping(destination, count, interval):
    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()

    # Set destination and send a ping one at a time until desired number of count is reached.
    transmitter.destination = destination
    transmitter.count = 1

    # Create a custom dictionary and initializing relevant key-value pairs.
    results = {
        'destination': destination,
        'packet_transmit': 0,
        'packet_receive': 0,
        'packet_loss_rate': 0.0,
        'packet_loss_count': 0,
        'rtt_min': float('inf'),
        'rtt_avg': 0.0,
        'rtt_max': float('-inf'),
        'start_time': None,
        'end_time': None,
        'elapsed_time': None
    }

    
    startTime = datetime.now()
    print(f'Pinging {destination}:')

    # Loop through each ping request and sum each value.
    for _ in range(count):
        result = transmitter.ping()
        stats = ping_parser.parse(result).as_dict()

        raw_output = result.stdout.strip()

        # Print ICMP reply for each ping request in real-time.
        reply_start = raw_output.find("Reply from")
        if reply_start != -1:
            reply_end = raw_output.find("\n", reply_start)
            icmp_reply = raw_output[reply_start:reply_end].replace("TTL", "Time-To-Live")
            print(icmp_reply)
        
        results['packet_transmit'] += stats['packet_transmit']
        results['packet_receive'] += stats['packet_receive']
        results['packet_loss_count'] += stats['packet_transmit'] - stats['packet_receive']

        results['rtt_min'] = min(results['rtt_min'], stats['rtt_min'])
        results['rtt_max'] = max(results['rtt_max'], stats['rtt_max'])
        results['rtt_avg'] += stats['rtt_avg']

        time.sleep(interval)
    
    print()
    endTime = datetime.now()

    # Calculate elapsed time using the start and end timestamps.
    elapsedTime = endTime - startTime
    total_seconds = elapsedTime.total_seconds() 
    formatted_elapsedTime = f"{int(total_seconds // 3600):02}:{int((total_seconds % 3600) // 60):02}:{total_seconds % 60:06.3f}"

    results['rtt_avg'] /= count
    results['packet_loss_rate'] = results['packet_loss_count'] / results['packet_transmit']
    results['start_time'] = startTime.strftime('%m/%d/%y %H:%M:%S')
    results['end_time'] = endTime.strftime('%m/%d/%y %H:%M:%S')
    results['elapsed_time'] = formatted_elapsedTime

    return results

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