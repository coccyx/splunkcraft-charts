#!/usr/bin/env python
# Needs Pillow & pycha & cairo

import splunklib.client as client, splunklib.results as results
import os
import cairo
import pycha.bar, pycha.pie, pycha.line
import minecraft.minecraft as minecraft
import minecraft.block as block
import threading
import time
from PIL import Image, ImageDraw, ImageFont

import png, array
import pprint

import cPickle

from ConfigParser import ConfigParser 

def splunkquery(splunkconf, q, et, lt, charttype, seriesfield, valuefield):
    service = client.connect( host=splunkconf['SPLUNK_HOST'], 
                                port=splunkconf['SPLUNK_PORT'], 
                                username=splunkconf['SPLUNK_USERNAME'], 
                                password=splunkconf['SPLUNK_PASSWORD'],
                                app=splunkconf['SPLUNK_APP'])
    r = service.jobs.oneshot(q, earliest_time=et, latest_time=lt)
    reader = results.ResultsReader(r)
    x = 0
    ret = [ ]
    out = [ ]
    for item in reader:
        pprint.pprint(item)
        series = item[seriesfield]
        # Find first non-internal value
        for (k,v) in item.iteritems():
            pprint.pprint(v)
            if k == valuefield:
                if charttype != 'pie':
                    out.append((x, float(v)))
                else:
                    ret.append((series, ((0, float(v)),)))
                x += 1
                break
    if charttype != 'pie':
        ret = (('dataset', tuple(out)),)
    else:
        ret = tuple(ret)
    pprint.pprint(ret)
    return ret

class MChart:
    def __init__(self, width=160, height=100, minecraft_host='192.168.99.100'):
        self.width = width
        self.height = height
        self.mc = minecraft.Minecraft.create(minecraft_host)
        self.chartnum = 1
        self.cache = False

    # Clear the rendering area
    def clear(self, x_offset, y_offset, z_offset, orientation):
        if orientation == 0:
            self.mc.setBlocks(x_offset-(self.width/2), 0+y_offset, z_offset, x_offset+(self.width/2), self.height+y_offset, z_offset, 0)
        else:
            self.mc.setBlocks(x_offset, 0+y_offset, z_offset-(self.width/2), x_offset, self.height+y_offset, z_offset+(self.width/2), 0)


    # Draw white background in rendering area
    def white(self, x_offset, y_offset, z_offset, orientation):
        if orientation == 0:
            self.mc.setBlocks(x_offset-(self.width/2), 0+y_offset, z_offset, x_offset+(self.width/2), self.height+y_offset, z_offset, block.Block(159, 0))
        else:
            self.mc.setBlocks(x_offset, 0+y_offset, z_offset-(self.width/2), x_offset, self.height+y_offset, z_offset+(self.width/2), block.Block(159, 0))


    def render(self, data, color='blue', charttype='verticalbar', title='title', file='output.png'):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)

        # dataSet = (
        #   ('dataSet 1', ((0, 1), (1, 3), (2, 2.5))),
        #   ('dataSet 2', ((0, 2), (1, 4), (2, 3))),
        #   ('dataSet 3', ((0, 5), (1, 1), (2, 0.5))),
        # )
        # dataSet = (
        #     ('dataset 1', ((0, 10), )),
        #     ('dataset 2', ((0, 15), )),
        #     ('dataset 3', ((0, 20), )),
        #     ('dataset 4', ((0, 25), )),
        #     ('dataset 5', ((0, 30), )),
        #     ('dataset 6', ((0, 20), )),
        #     ('dataset 7', ((0, 40), )),
        #     )
        # pprint.pprint(dataSet)

        colors = ('#ff0000', '#00ff00', '#0000ff',
                      '#00ffff', '#000000', '#ff00ff',
                      '#ffff00')
        options = {
            'legend': {'hide': True},
            'background': {'color': '#ffffff',
                           'chartColor': '#ffffff',
                           'baseColor': '#ffffff',
                           'lineColor': '#000000'},
            # 'colorScheme': {'name': 'fixed', 'args': {'colors': colors}},
            'colorScheme': {
                'name': 'gradient',
                'args': {
                    'initialColor': color,
                },
            },
            'title': title,
            # 'axis': {
            #     'y': { 'label': data[0][0] },
            # }
            # 'axis': {
            #     'x': { 'hide': True }
            # }
            # 'axis': {
            #     'x': {
            #         'ticks': [{'v': 0, 'label': '1'},
            #                     {'v': 1, 'label': '2'},
            #                     {'v': 2, 'label': '3'},
            #                     {'v': 3, 'label': '4'},
            #                     {'v': 4, 'label': '5'},
            #                     {'v': 5, 'label': '6'},
            #                     {'v': 6, 'label': '7'},
            #                     {'v': 7, 'label': '8'}],
            #         'rotate': 25
            #     }
            # }
        }

        outdata = data
        if charttype in ['verticalbar', 'horizontalbar', 'line', 'pie']:
            if charttype == 'verticalbar':
                chart = pycha.bar.VerticalBarChart(surface, options)
            elif charttype == 'horizontalbar':
                chart = pycha.bar.HorizontalBarChart(surface, options)
            elif charttype == 'line':
                chart = pycha.line.LineChart(surface, options)
            elif charttype == 'pie':
                chart = pycha.pie.PieChart(surface, options)
                # newdata = tuple([(str(x[0]), ((0, x[1]),)) for x in data[0][1]])
                # outdata = newdata
                # pprint.pprint(outdata)
            chart.addDataset(outdata)
            chart.render()
            surface.write_to_png(file)
        elif charttype == 'singlevalue':
            val = data[0][1][0][1]
            pprint.pprint(val)
            image = Image.new("RGB", (self.width,self.height), (255,255,255))
            draw = ImageDraw.Draw(image)
            try:
                font = ImageFont.truetype("/data/OpenSans-Regular.ttf", 15)
            except IOError:
                font = ImageFont.truetype("OpenSans-Regular.ttf", 15)
            # draw text, full opacity1
            tw, th = draw.textsize(title, font=font)
            draw.text(((self.width/2 - tw/2), 10), title, font=font, fill=(0,0,0))

            try:
                font = ImageFont.truetype("/data/OpenSans-Regular.ttf", 36)
            except IOError:
                font = ImageFont.truetype("OpenSans-Regular.ttf", 36)
            tw, th = draw.textsize(str(val), font=font)
            draw.text(((self.width/2 - tw/2), 50), str(val), font=font, fill=(0,0,0))
            image.save(file, "PNG")


    def draw(self, x_offset, y_offset, z_offset, orientation, mirrored, file='output.png'):
        commands = 0
        # Read from cache
        if self.cache:
            cache = self.cache
        else:
            cache = [ block.Block(159,0) for x in range(self.width * self.height) ]
        # try:
        #     f = open("cache_%s.dat" % self.chartnum, "rb")
        #     cache = cPickle.load(f)
        # except (AttributeError, IOError, EOFError) as e:
        #     cache = [ block.Block(159,0) for x in range(self.width * self.height) ]
        print 'mirrored: %s' % mirrored
        # self.clear(x_offset, y_offset, z_offset, orientation)
        # return

        # Check if we've already drawn something
        commands += 1        
        if self.mc.getBlock(x_offset, y_offset, z_offset) == block.AIR:
            self.white(x_offset, y_offset, z_offset, orientation)
            cache = [ block.Block(159,0) for x in range(self.width * self.height) ]

        reader = png.Reader(file)
        w, h, pixels, metadata = reader.read_flat()

        for y in range(h):
            row = [ ]
            for x in range(w):
                pixel_byte_width = 3
                pixel = pixels[(x * pixel_byte_width) + (y * self.width * pixel_byte_width) : 
                            ((x+1) * pixel_byte_width) + (y * self.width * pixel_byte_width) ]

                # Grab the top 2 bits
                r = pixel[0] >> 6
                g = pixel[1] >> 6
                b = pixel[2] >> 6

                # Add up total of all bits to get a relative brightness
                tot = r+g+b
                if tot <= 2:
                    if b >= 1:
                        # Set Blue
                        # b = block.WOOL.withData(11)
                        b = block.Block(159, 11)
                    elif r >= 1:
                        # Set Red
                        # b = block.WOOL.withData(14)
                        b = block.Block(159, 14)
                    elif g >= 1:
                        # Set Green
                        # b = block.WOOL.withData(13)
                        b = block.Block(159, 13)
                    else:
                        # Set Black
                        # b = block.WOOL.withData(15)
                        b = block.Block(159, 15)
                elif tot <= 5:
                    # Set Light Grey
                    # b = block.WOOL.withData(8)
                    b = block.Block(159, 15)
                elif tot <= 8:
                    # Set Grey
                    # b = block.WOOL.withData(7)
                    b = block.Block(159, 7)
                else:
                    # Set White
                    # b = block.WOOL.withData(0)
                    b = block.Block(159, 0)

                # Every fifth row
                if y % 10 == 3:
                    # Every 20th block
                    if x % 20 == 3 or x % 20 == 13:
                        b = block.GLOWSTONE_BLOCK
                if y % 10 == 8:
                    if x % 20 == 8 or x % 20 == 18:
                        b = block.GLOWSTONE_BLOCK

                if cache[x+(y*self.width)] != b:
                    row.append((x, b))
                cache[x+(y*self.width)] = b

            # Now lets scan through all the blocks that were cache misses and group them into series
            grouped_row = [ ]
            if len(row) > 1:
                first_x = row[0][0]
                last_x = row[0][0]
                last_b = row[0][1]
                for (x, b) in row[1:]:
                    # Check to make sure we're a contiguous series and we're the same block
                    if x != last_x+1 or b != last_b:
                        grouped_row.append((first_x, last_x, last_b))
                        first_x = x
                    last_x = x
                    last_b = b
                grouped_row.append((first_x, last_x, last_b))

            # Now iterate through grouped rows and draw them
            for (x1, x2, b) in grouped_row:
                if orientation == 0:
                    if mirrored == False:
                        self.mc.setBlocks(self.width-x1-(self.width/2), self.height-y+y_offset, z_offset, self.width-x2-(self.width/2), self.height-y+y_offset, z_offset, b)
                    else:
                        self.mc.setBlocks(x1-(self.width/2), self.height-y+y_offset, z_offset, x2-(self.width/2), self.height-y+y_offset, z_offset, b)
                elif orientation == 1:
                    if mirrored == False:
                        self.mc.setBlocks(x_offset, self.height-y+y_offset, self.width-x1-(self.width/2), x_offset, self.height-y+y_offset, self.width-x2-(self.width/2), b)
                    else:
                        self.mc.setBlocks(x_offset, self.height-y+y_offset, x1-(self.width/2), x_offset, self.height-y+y_offset, x2-(self.width/2), b)
                commands += 1

        self.cache = cache
        # f = open('cache_%s.dat' % self.chartnum, 'wb')
        # cPickle.dump(cache, f)
        self.chartnum += 1
        print "commands sent: %s" % commands

def work(mchart, chart):
    print "Doing work!"
    try:
        data = splunkquery(splunkconf, chart['QUERY'], chart['ET'], chart['LT'], chart['TYPE'], chart['SERIESFIELD'], chart['VALUEFIELD'])
        renderkw = dict([ (setting[0], chart[setting[1]] ) for setting in RENDER_SETTINGS ])
        renderkw['data'] = data
        drawkw = dict([ (setting[0], chart[setting[1]] ) for setting in DRAW_SETTINGS ])

        mchart.render(**renderkw)
        mchart.draw(**drawkw)
    except KeyError:
        pass


if __name__ == '__main__':
    c = ConfigParser()
    STRING_SETTINGS = ['COLOR', 'ET', 'LT', 'QUERY', 'TITLE', 'TYPE']
    INT_SETTINGS = ['ORIENTATION', 'XOFFSET', 'YOFFSET', 'ZOFFSET', 'TIMER']
    BOOLEAN_SETTINGS = ['MIRROR']

    RENDER_SETTINGS = [ ('color', 'COLOR'), ('charttype', 'TYPE'), ('title', 'TITLE') ]
    DRAW_SETTINGS = [ ('x_offset', 'XOFFSET'), ('y_offset', 'YOFFSET'), ('z_offset', 'ZOFFSET'), ('orientation', 'ORIENTATION'), ('mirrored', 'MIRROR') ]
    if os.path.exists('chart.conf'):
        c.read(['chart.conf'])

        charts = [ ]

        sections = c.sections()
        for section in [ section for section in sections if section != 'splunk' and section != 'minecraft']:
            t = dict(c.items(section))
            o = { }
            for (k, v) in t.iteritems():
                if k.upper() in INT_SETTINGS:
                    o[k.upper()] = int(v)
                elif k.upper() in BOOLEAN_SETTINGS:
                    o[k.upper()] = bool(int(v))
                else:
                    o[k.upper()] = v
            charts.append(o)

        t = dict(c.items('splunk'))
        splunkconf = { }
        for (k,v) in t.iteritems():
            splunkconf[k.upper()] = v

        t = dict(c.items('minecraft'))
        minecraft_host = t['minecraft_host']
    else:
        splunkconf = {
            'SPLUNK_HOST': 'demo-minecraft.splunkoxygen.com',
            'SPLUNK_PORT': 8089,
            'SPLUNK_USERNAME': 'Coccyx80',
            'SPLUNK_PASSWORD': 'changeme',
            'SPLUNK_APP': 'mc_sandbox'
        }

        for v in ('SPLUNK_HOST', 'SPLUNK_PORT', 'SPLUNK_USERNAME', 'SPLUNK_PASSWORD'):
            temp = os.getenv(v, None)
            if temp != None:
                splunkconf[v] = t

        # data = splunkquery(splunkconf, 'search eventtype=splunkcraft2016 | timechart span=1d dc(player)', '-7d@d', '-0d@d')

        chartslist = sorted([ (k, v) for (k, v) in os.environ.iteritems() if k.startswith('CHART') ])
        charts = [ { } ]
        current = 1
        for x in chartslist:
            terms = x[0].split('_')
            # Check to see if we're still on the current numbered chart
            if int(terms[1]) != current:
                curcurrent = current
                # We've advanced
                current = int(terms[1])
                for z in range(curcurrent, current):
                    charts.append( { } )
            if terms[2] in INT_SETTINGS:
                charts[current-1][terms[2]] = int(x[1])
            elif terms[2] in BOOLEAN_SETTINGS:
                charts[current-1][terms[2]] = bool(int(x[1]))
            else:
                charts[current-1][terms[2]] = x[1]

        minecraft_host = os.getenv('MINECRAFT_HOST', '192.168.99.100')
        

    for chart in charts:
        # pprint.pprint(chart)
        mchart = MChart(minecraft_host=minecraft_host)
        work(mchart, chart)
        print 'Starting timer for %s' % chart['TITLE']
        t = threading.Timer(float(chart['TIMER']), work, [mchart, chart ])
        t.daemon = True
        t.start()

    while True:
        time.sleep(1.0)

    # mchart.render(data, 'red', 'verticalbar', 'Users last 7d')
    # mchart.draw(0, 0, 80, 0, False)
    # mchart.render(data, 'blue', 'line', 'Users last 7d')
    # mchart.draw(0, 0, -80, 0, True)
    # mchart.render(data, 'green', 'horizontalbar', 'Users last 7d')
    # mchart.draw(-80, 0, 0, 1, False)
    # # mchart.render(data, 'black', 'pie')
    # # mchart.draw(80, 0, 0, 1, True)
    # mchart.render(1000, 'black', 'singlevalue', 'Current users')
    # mchart.draw(80, 0, 0, 1, True)
    # mchart.clear(0, 0, 80, 0)
    # mchart.clear(0, 0, -80, 0)
    # mchart.clear(-80, 0, 0, 1)
    # render(data, 0, 0, -80)
    # render(data, -80, 0, 0)
    # render(data, 80, 0, 0)
    # render(data, 0, 100, 160)
