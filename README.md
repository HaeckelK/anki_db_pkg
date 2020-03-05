# winbackground_pkg

Basic functions to change Windows wallpaper.

## Installation

winbackground_pkg is not yet on pip so cannot be installed via pip. Instead the repository may be cloned.

```bash
git clone https://github.com/HaeckelK/winbackground_pkg.git
```

## Requirements
Windows 10

## Usage

Assuming you have a folder called C:\\wallpapers with files test_image1.jpg to test_image4.jpg.

Choose background at random from files in a folder:
```python
from background.background import Background

bk = Background()
bk.change('C:\\wallpapers\\test_image.jpg')
```

Choose background at random from files in a folder:
```python
from background.background import Background

bk = Background()
bk.random_from_folder('C:\\wallpapers')
```

Choose background at random from files in a list:
```python
from background.background import Background

bk = Background()
files = ['C:\\wallpapers\\test_image.jpg', 'C:\\wallpapers\\test_image2.jpg',
         'C:\\wallpapers\\test_image3.jpg', 'C:\\wallpapers\\test_image4.jpg']
        
bk.random_from_list(files)
```

Prevent detailed command line printing by setting verbose = False:
```python
from background.background import Background

bk = Background()
bk.verbose = False
bk.change('C:\\wallpapers\\test_image4.jpg')
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](LICENSE.md)