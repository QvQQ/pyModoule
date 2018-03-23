#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib import request, parse
import json, os

class songdl(object):

    def search(self, *, songname, artist=None):
        url = r'http://s.music.163.com/search/get'
        urldata = parse.urlencode([
                    ('s', songname),
                    ('type', 1),
                    ('filterDj', 'True'),
                    ('limit', 50),
                    ('offset', 0)]).encode()
        with request.urlopen(url, data = urldata) as f:
            oridata = f.read().decode()
        dictdata = json.loads(oridata)
        if len(dictdata) != 2 or 'result' not in dictdata or 'songCount' not in dictdata['result'] or dictdata['result']['songCount'] <= 0 or 'songs' not in dictdata['result'] or len(dictdata['result']['songs']) <= 0:
                    print(dictdata)
                    print('Invalid data!')
                    return None
        for d in dictdata['result']['songs']:
            print(d['artists'][0]['name'])
            if d['artists'][0]['name'] == artist or artist == None:
                return {'id':d['id'], 'artist':d['artists'][0]['name'], 'name':d['name']}
        print('Song not found!')
        return None
        
    def downloadsong(self, *, song, localdir, dlreport=None):
        print('Downloading...')
        url = r'http://music.163.com/song/media/outer/url?id={}.mp3'.format(song['id'])
        url2 = r'http://music.163.com/api/song/enhance/download/url?br=320000&id={}'.format(song['id'])
        filepath = '{0}{1} - {2}.mp3'.format(localdir, song['name'], song['artist'])
        print(filepath)
        if not os.path.exists(filepath):
            request.urlretrieve(url, filepath, dlreport)
        print('Downloaded.')
        return filepath

    def getlyrics(self, song):
        print('Getting...')
        url = r'http://music.163.com/api/song/media?id={}'.format(song['id'])
        with request.urlopen(url=url) as f:
            oridata = f.read().decode()
        dictdata = json.loads(oridata)
        if 'nolyric' in dictdata and dictdata['nolyric'] == True:
            return '纯音乐，请欣赏'
        if 'lyric' not in dictdata:
            return '暂时没有歌词!'
            return None
        lyrics = dictdata['lyric']
        return lyrics







        
