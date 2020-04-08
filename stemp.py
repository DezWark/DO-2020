#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import pygame
import random
import platform

def stemp(screenresolution, fullscreen, verim, keym, beacon):
    # -*- coding: utf-8 -*-
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    PINK = (230, 50, 230)
    Upd = True
    os = platform.system()
    if (sys.platform.startswith("win")):
        import pywintypes
        from win32 import win32gui
        import win32con
    else:
        import os
    pygame.init()                     
    if fullscreen:
        infos = pygame.display.Info()
        scr_w = infos.current_w
        scr_h = infos.current_h
        screen = pygame.display.set_mode((scr_w, scr_h), pygame.FULLSCREEN)
    else:
        scr_w = screenresolution[0]
        scr_h = screenresolution[1]
        screen = pygame.display.set_mode((scr_w, scr_h)) 
    background = pygame.Surface(screen.get_size()) 
    background.fill(BLACK) 
    background = background.convert() 
    screen.blit(background, (0,0)) 
    clock = pygame.time.Clock() 
    mainloop = True
    FPS = 30
    playtime = 0.0
    while mainloop:
        milliseconds = clock.tick(FPS)
        playtime += milliseconds / 1000.0
        color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        if Upd:
            for n in range(scr_w//2):
                pygame.draw.line(screen, WHITE, [n*2,0], [n*2,scr_h], 1)
            if verim:
                h = (scr_h/2)//(2*verim+1)
                for v in range(verim):
                    pygame.draw.rect(screen, color, (0,2*v*h,scr_w,h))
                pygame.draw.rect(screen, color, (0,2*verim*h,scr_w,h))
            Upd = False
        if beacon:
            time.sleep(beacon)
            if (sys.platform.startswith("linux")):
                os.system('gdbus call --session --dest org.gnome.SettingsDaemon.Power --object-path /org/gnome/SettingsDaemon/Power --method org.freedesktop.DBus.Properties.Set org.gnome.SettingsDaemon.Power.Screen Brightness "<int32 0>"')
                time.sleep(beacon)
                os.system('gdbus call --session --dest org.gnome.SettingsDaemon.Power --object-path /org/gnome/SettingsDaemon/Power --method org.freedesktop.DBus.Properties.Set org.gnome.SettingsDaemon.Power.Screen Brightness "<int32 100>"')
            else:
                win32gui.SendMessage(win32con.HWND_BROADCAST,win32con.WM_SYSCOMMAND, win32con.SC_MONITORPOWER, 2)
                time.sleep(beacon)
                win32gui.SendMessage(win32con.HWND_BROADCAST,win32con.WM_SYSCOMMAND, win32con.SC_MONITORPOWER, -1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
            elif event.type == pygame.KEYDOWN:
                if keym:
                    h = scr_h//16
                    for v in range(8):
                        if (event.key&(1<<v)):
                            pygame.draw.rect(screen, BLACK, (0,(2*v+1)*h,scr_w,h))
                        else:
                            pygame.draw.rect(screen, BLACK, (0,(2*v)*h,scr_w,h))
                Upd = False
                if event.key == pygame.K_ESCAPE:
                    mainloop = False
            elif event.type == pygame.KEYUP:
                Upd = True
        pygame.display.set_caption("press ESC to quit. FPS: %.2f (%ix%i), time: %.2f seonds" % (clock.get_fps(), scr_w, scr_h, playtime))
        pygame.display.flip()
    print("Played for %.2f seconds" % playtime)
    pygame.quit()
    return playtime

if __name__ == '__main__':
    k = False
    b = 0
    v = 0
    if len(sys.argv) > 1:
        for pn in range(len(sys.argv)):
            if (sys.argv[pn] == "-v"):
                if (pn+1 < len(sys.argv)):
                    v = int(sys.argv[pn+1])
            if (sys.argv[pn] == "-b"):
                if (pn+1 < len(sys.argv)):
                    b = int(sys.argv[pn+1])//2
            if (sys.argv[pn] == "-k"):
                k = True
    stemp((1280,800),True,v,k,b)
