# AWS Icon Set generation for Inkscape

## Installation

Download or clone this repository
```
git clone https://github.com/reallyasi9/aws-inkscape-symbols
```

## Generation of symbols

Download the latest Assets Package
from the [AWS Simple Icons](https://aws.amazon.com/architecture/icons/)
page.

Run:

```
python build.py /path/to/downloaded.zip
```

This will create all of the AWS symbols in the `target` subdirectory. Optionally pass the `--output` (short form: `-o`) flag to set a different output directory. For usage, try `--help`.

## Using the symbols with inkscape

Create a `symbols` directory in your Inkscape configuration directory if it doesn't exist (defaults to `~\AppData\Roaming\inkscape` on Windows, `~/.config/inkscape` on Linux/MacOS) and copy the needed symbol sets to that directory.

## References/Inspiration

The core of the code comes from [Will Thames](https://github.com/willthames/aws-inkscape-symbols). I just slapped some varnish on it.

## License

This repository is currently offered under the MIT License
Different terms almost certainly apply to your usage of the AWS
Icon Sets. At the time of writing, AWS
[haven't explicitly stated those terms](https://forums.aws.amazon.com/thread.jspa?messageID=792596).

Once those terms become clear, I might start including the symbols
alongside the generation code (at which point the license might need
to change).
