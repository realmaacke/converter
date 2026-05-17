## Converter

Systemd serivce to transcode media files into a HVEC format.
The program runs on a loop every hour.
The first argument of the program takes "amd" or "nvidia".
The second argument is the path of where the program is to search.


### Configuration
1. Change settings in the media-compressor.service file, (i.e, name, python path, actual path, gpu type, ...)
2. cp service file to **/etc/systemd/system/media-compressor.service**
3. sudo systemctl daemon-reload
4. sudo systemctl enable media-compressor.service
5. sudo systemctl start media-compressor.service
6. sudo systemctl status media-compressor.service
