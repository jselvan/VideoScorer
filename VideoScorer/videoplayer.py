try:
    from msvcrt import getch
except ImportError:
    def getch(): raise NotImplementedError
from vlc import Instance, VideoMarqueeOption, EventType

class VideoPlayer:
    def __init__(self):
        self.instance = Instance(["--sub-source=marq"])
        player = self.instance.media_player_new()

        # Some marquee examples.  Marquee requires '--sub-source marq' in the
        # Instance() call above, see <http://www.videolan.org/doc/play-howto/en/ch04.html>
        player.video_set_marquee_int(VideoMarqueeOption.Enable, 1)
        player.video_set_marquee_int(VideoMarqueeOption.Size, 24)  # pixels
        # player.video_set_marquee_int(VideoMarqueeOption.Position, 'bottom')
        player.video_set_marquee_int(VideoMarqueeOption.Timeout, 0)  # millisec, 0==forever
        player.video_set_marquee_int(VideoMarqueeOption.Refresh, 1000)  # millisec (or sec?)
        player.video_set_marquee_string(VideoMarqueeOption.Text, bytes('%Y-%m-%d  %H:%M:%S','utf-8'))

        # Some event manager examples.  Note, the callback can be any Python
        # callable and does not need to be decorated.  Optionally, specify
        # any number of positional and/or keyword arguments to be passed
        # to the callback (in addition to the first one, an Event instance).
        event_manager = player.event_manager()
        event_manager.event_attach(EventType.MediaPlayerEndReached, self.end_callback)
        self.player = player
        
        self.keybindings = {
            ' ': self.player.pause,
            '+': self.sec_forward,
            '-': self.sec_backward,
            '.': self.frame_forward,
            ',': self.frame_backward,
            'f': self.player.toggle_fullscreen
        }

    def end_callback(self, event):
        print('End of media stream (event %s)' % event.type)

    @property
    def mspf(self):
        """Milliseconds per frame"""
        return int(1000 // (self.player.get_fps() or 25))

    def sec_forward(self):
        """Go forward one sec"""
        self.player.set_time(self.player.get_time() + 1000)

    def sec_backward(self):
        """Go backward one sec"""
        self.player.set_time(self.player.get_time() - 1000)

    def frame_forward(self):
        """Go forward one frame"""
        self.player.set_time(self.player.get_time() + self.mspf())

    def frame_backward(self):
        """Go backward one frame"""
        self.player.set_time(self.player.get_time() - self.mspf())

    def listen(self):
        while True:
            k = getch()
            print('> %s' % k)
            if k in self.keybindings:
                self.keybindings[k]()
            elif k.isdigit():
                    # jump to fraction of the movie.
                self.player.set_position(float('0.'+k))
    
    def play_movie(self, movie):
        media = self.instance.media_new(movie)
        self.player.set_media(media)
        self.player.play()