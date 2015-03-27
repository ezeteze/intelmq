from datetime import datetime
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils

class malc0deParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report:
            for row in report.split('\n'):
                
                row = row.strip()              

                if len(row) == 0 or row.startswith('#'):
                    continue
                
                row = row.split()
                event = Event()

                columns = ["source_ip", "source_time"]
                
                for key, value in zip(columns, row):    
                    if key == "source_time":
                        value = datetime.utcfromtimestamp(int(value)).strftime('%Y-%m-%d %H:%M:%S') + " UTC"
                    
                    event.add(key, value.strip())

                event.add('feed', 'zeus')
                event.add('feed_url', 'https://zeustracker.abuse.ch/blocklist.php?download=badips')
                event.add('type', 'zeus')
                
                event = utils.parse_source_time(event, "source_time")
                event = utils.generate_observation_time(event, "observation_time")
                event = utils.generate_reported_fields(event)

                self.send_message(event)

        self.acknowledge_message()


if __name__ == "__main__":
    bot = malc0deParserBot(sys.argv[1])
    bot.start()

