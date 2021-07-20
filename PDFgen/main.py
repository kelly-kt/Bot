import Config
import discord_db
import analyse
import popularity
import send_email


from fpdf import FPDF

title = 'PROFANITY REPORT'


class PDF(FPDF):
    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Calculate width of title and position
        w = self.get_string_width(title) + 6
        self.set_x((210 - w) / 2)
        # Colors of frame, background and text
        self.set_draw_color(0, 80, 180)
        self.set_fill_color(230, 230, 0)
        self.set_text_color(220, 50, 50)
        # Thickness of frame (1 mm)
        self.set_line_width(1)
        # Title
        self.cell(w, 9, title, 1, 1, 'C', 1)
        # Line break
        self.ln(10)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def chapter_title(self, num, label):
        # Arial 12
        self.set_font('Arial', '', 18)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 6, 'Chapter %d : %s' % (num, label), 0, 1, 'L', 1)
        # Line break
        self.ln(4)

    def chapter_body(self, name):
        # Times 12
        self.set_font('Arial', '', 12)
        # Output justified text
        self.multi_cell(0, 5, name)
        # Line break
        self.ln()

    def add_section(self, chap, num, label):
        # Arial 12
        self.set_font('Arial', '', 14)
        # Title
        self.cell(0, 6, '{}.{}. {}'.format(chap, num, label), 0, 1, 'L', 1)
        # Line break
        self.ln(4)

    def add_text(self, text):
        # Output justified text
        self.multi_cell(0, 5, text)
        # Line break
        self.ln()

    def add_bullet_list(self, items):
        # Output justified text
        for item in items:
            #          self.multi_cell(0, 5, u'\u2022 '+item)
            self.multi_cell(0, 5, item)
        # Line break
        self.ln()

    def print_chapter(self, num, title, name):
        self.add_page()
        self.chapter_title(num, title)
        self.chapter_body(name)

    def add_profanity_channel_user(self, num, results):
        section_id = 1
        print('  Generating Chapter {} (bad language per user)'.format(num))
        self.print_chapter(num, "User profanity report",
                           "This chapter contains a list of all users who have posted profanity to the Discord Server")
        for user in results:
            section_title = "Summary information for {}".format(user)
            summary_paragraph = '{} posted a total of {} messages with profanity.\nThe messages posted are listed below:'.format(
                user, results[user]['count'])

            print(section_title)
            print(summary_paragraph)
            self.add_text(section_title)
            self.add_text(summary_paragraph)
            for msg in results[user]['messages']:
                msg = msg.encode('ascii', 'ignore').decode('ascii')
                self.add_text(' - '+msg)
                print(" -", msg)
            print("----------")
            section_id += 1

    def add_profanity_channel_chapter(self, num, results):
        section_id = 1
        print('  Generating Chapter {} (bad language per channel)'.format(num))
        self.print_chapter(num, "Channel profanity report",
                           "This chapter contains a list of all channels on the Discord server where profanity has been posted")
        for channel in results:
            section_title = "Summary information for channel {}".format(
                channel)
            summary_paragraph = 'A total of {} messages with profanity have been posted in this channel.\nThe messages posted are listed below:'.format(
                results[channel]['count'])

            self.add_section(num, section_id, section_title)
            self.add_text(summary_paragraph)
            channelmsg = results[channel]['messages']
            bullet_point = " -- "
            newlist = [bullet_point + x for x in channelmsg]
            self.add_bullet_list(newlist)
            print(newlist)
            section_id += 1

    def add_popularity_report_chapter(self, num, results):
        section_id = 1
        print('  Generating Chapter {} (popularity topic results)'.format(num))
        self.print_chapter(
            num, 'Channel Content Popularity Report', 'This chapter contains....')
        for channel in results:
            section_title = 'Summary information for {}'.format(channel)
            summary_paragraph = results[channel]['popularity']

            print(summary_paragraph)
            self.add_section(num, section_id, section_title)
            self.add_text(summary_paragraph)
            section_id += 1

    def create_report(self, bad_users, bad_channels, popularity):
        print('Generating PDF report')
        self.set_author('Discord Analysis Tool')
        self.print_chapter(1, 'Introduction', 'The analysis tool helps you generate report including profanity report and trending topic report. It will automatically send an email to you with the pdf report attached at the same time.')
        self.add_profanity_channel_user(2, bad_users)
        self.add_profanity_channel_chapter(3, bad_channels)
        self.add_popularity_report_chapter(4, popularity)

# ######### INSTRUCTION #############
# Install the library by following command in the shell
# pip install fpdf
# The fpdf only supports txt to pdf convertion.
# There is the panda library to convert the json data to text file, then the txt file can be used for the pdf generation. To install panda in the shell:
# pip install pandas

# resources:
# https://github.com/reingart/pyfpdf/blob/master/docs/Tutorial.md
# https://datatofish.com/json-to-text-file-python/


# MongoDB

def initialise_program():
    print("Initialising Analysis Tool")
    Config.load_configuration('config.ini')

    discord_db.initialise_db(Config.config["database"]["mongo"])


def main():
    initialise_program()

    # Retrieve message from database
    good_messages = discord_db.retrieve_messages_since('test')
    bad_messages = discord_db.retrieve_bad_messages_since('test')

    # Reorganise messages for analysis/reporting
    messages_list = analyse.process_messages(good_messages)
    (bad_users, bad_channels) = analyse.process_bad_messages(bad_messages)

    print('----------------------------------------------')
    print('MESSAGES TO ANALYSE FOR POPULARITY')
    # need to call a function to analyse messages in messages_list and return analysis of popularity
    for channel in messages_list:
        print('analysining channel', channel)
        messages_list[channel]['popularity'] = popularity.popularity_report(
            messages_list[channel]['messages'])

    print('----------------------------------------------')

    title = 'DISCORD SERVER ANALYSIS REPORT'

    pdf = PDF()
    #pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)

    pdf.set_title(title)

    pdf.create_report(bad_users, bad_channels, messages_list)

    pdf.output('report_demo.pdf', 'F')

    send_email.send_report('report_demo.pdf')


# if __main__ == '__main__':
main()
