# ha_mozillatts
Mozilla TTS Custom Component to work with [synesthesiam/docker-mozillatts](https://github.com/synesthesiam/docker-mozillatts) 
Only supports en-us language and default (en-us female) voice

### Configuration
* host: mozillatts host (default localhost)
* port: mozillatts port (default 5002)
```
tts:
- platform: mozillatts
  host: mymozillahost
  port: 5002
```
