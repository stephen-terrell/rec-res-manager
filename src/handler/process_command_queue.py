from src.event.process_command_queue_event import ProcessCommandQueueEvent


def handler(event, context):
    event_handler = ProcessCommandQueueEvent(event, context)

    event_handler.handle()


if __name__ == "__main__":
    handler({}, {})
