import argparse
import sys
from confluent_kafka import KafkaException, KafkaError
from confluent_kafka.admin import AdminClient, NewTopic

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='ProgramName',
        description='What the program does',
        epilog='Text at the bottom of help')
    parser.add_argument('topic_name')
    parser.add_argument('bootstrap_server')
    args = parser.parse_args()

    admin_client = AdminClient({
        "bootstrap.servers": args.bootstrap_server
    })
    creating_flag = True
    topic_list = [NewTopic(topic=args.topic_name, num_partitions=1, replication_factor=1)]
    create_cmd = admin_client.create_topics(topic_list)[args.topic_name]
    try:
        while creating_flag:
            res = create_cmd.result()
            if create_cmd.done():
                break
    except KafkaException as ke:
        if ke.args[0].code() == KafkaError.TOPIC_ALREADY_EXISTS:
            sys.exit(0)
        else:
            raise (ke)
    sys.exit(0)
