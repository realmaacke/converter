## Converter

Encodes mkv files with HEVC to reduce disk usage.
the .service file is put into **/etc/systemd/system/media-compressor.service**
in the service file, change the arguments to match you're specific path.


run theese files to get the service running:
```
sudo systemctl daemon-reload
sudo systemctl enable compressor.service
sudo systemctl start compressor.service
``