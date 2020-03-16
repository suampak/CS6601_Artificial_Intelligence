class PriorityQueue(object):
    def __init__(self):
        self.queue = [] # [priority, value]
        self.index = 0

    def pop(self):
        if self.index > 0:
            ret = self.queue[0]
            self.index -= 1
            self.queue[0] = self.queue[self.index]
            self.__fixDown(0)
            return ret

        raise Exception('Queue is empty')

    def append(self, node):
        if len(self.queue) == self.index:
            self.queue.append(node)
        else:
            self.queue[self.index] = node

        self.__fixUp(self.index)
        self.index += 1

    def size(self):
        return self.index

    def clear(self):
        self.queue = []
        self.index = 0

    def top(self):
        return self.queue[0]

    def __fixUp(self, index):
        pa = (index-1)>>1
        while index > 0 and self.queue[index][0] < self.queue[pa][0]:
            self.queue[index], self.queue[pa] = self.queue[pa], self.queue[index]
            index = pa
            pa = (index-1)>>1

    def __fixDown(self, index):
        ch = 2*index+1
        while self.index > ch:
            if self.index > ch+1 and self.queue[ch][0] > self.queue[ch+1][0]:
                ch += 1
            if self.queue[index][0] > self.queue[ch][0]:
                self.queue[index], self.queue[ch] = self.queue[ch], self.queue[index]
                index = ch
                ch = 2*index+1
            else:
                break
