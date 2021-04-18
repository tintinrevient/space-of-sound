# Sound

## Magenta

* https://github.com/magenta/magenta/tree/master/magenta/models/music_vae
* https://colab.research.google.com/github/magenta/magenta-demos/blob/master/colab-notebooks/MusicVAE.ipynb
* https://notebook.community/magenta/magenta-demos/colab-notebooks/MusicVAE

## HPC

* RTX2080Ti
* RTX6000
* TeslaV100
* TeslaP100

```bash
sbatch -p gpu --gres=tmpspace:50G --gpus-per-node=RTX6000:1 --time 48:00:00 --mem 50G train16.sh
```

```bash
srun -p gpu -c 2 --gres=tmpspace:50G --gpus-per-node=TeslaV100:1 --time 02:00:00 --mem 100G --pty bash
```

```bash
squeue -u szhao
```

* https://github.com/OceanParcels/UtrechtTeam/wiki/How-to-run-parcels-on-gemini-and-cartesius
* https://hpc.op.umcutrecht.nl/
* https://hpc.op.umcutrecht.nl/pun/sys/dashboard
* https://wiki.bioinformatics.umcutrecht.nl/HPC
* https://wiki.bioinformatics.umcutrecht.nl/bin/view/HPC/FirstTimeUsers
* https://wiki.bioinformatics.umcutrecht.nl/bin/view/HPC/HowToS
* https://drive.google.com/drive/folders/0B1UNon8v26XsV2xJQ3J3ekVXWlU
* https://wiki.bioinformatics.umcutrecht.nl/pub/HPC/FirstTimeUsers/pi_in_python.pdf

## Tensorflow

```python
import tensorflow as tf

tf.test.is_gpu_available(
    cuda_only=False, min_cuda_compute_capability=None
)
```

* https://www.tensorflow.org/api_docs/python/tf/test/is_gpu_available

## References
* https://interactiveaudiolab.github.io/
* https://pypi.org/project/miditk-smf/
* https://pypi.org/project/py-midi/
* https://ismir.net/resources/software-tools/
* http://jmir.sourceforge.net/
* https://github.com/librosa/librosa/
* https://librosa.org/doc/latest/index.html
* https://nbviewer.jupyter.org/gist/bmcfee/8632059
* https://github.com/MTG
* https://staff.aist.go.jp/m.goto/RWC-MDB/
* http://www.piano-midi.de/
* http://ismir.net/resources/
* https://www.ismir2020.net/
* https://transactions.ismir.net/
* https://transactions.ismir.net/collections/special/20th-anniversary-of-ismir/
* https://www.oxfordmusiconline.com/
* https://web.stanford.edu/group/htgg/cgi-bin/drupal/
* https://devhints.io/homebrew
* https://boblsturm.github.io/aimusic2020/
* https://gudgud96.github.io/2020/10/17/ismir_2020/
* https://dblp.uni-trier.de/db/conf/ismir/index.html
* https://www.music-ir.org/mirex/wiki/MIREX_HOME
* http://millionsongdataset.com/
* http://magnatune.com/
* https://www.allmusic.nl/
* http://www.liederenbank.nl/
* https://www.classicalarchives.com/newca/#!/
* http://esac-data.org/
* http://kern.ccarh.org/
* http://web.mit.edu/music21/#
* https://www.sonicvisualiser.org/
* https://code.soundsoftware.ac.uk/projects/c4dm-chord-transcriptions
* https://ddmal.music.mcgill.ca/research/The_McGill_Billboard_Project_(Chord_Analysis_Dataset)/
* https://www.humdrum.org/
* https://en.wikipedia.org/wiki/Music_in_psychological_operations
* https://www.onlineconverter.com/midi-to-flac
* https://en.wikipedia.org/wiki/Diegesis
* https://www.musiccognition.osu.edu/
* https://shellyknotts.wordpress.com/
* https://jonmccormack.info/
* https://www.wired.co.uk/article/making-music-with-live-computer-code-
* http://openmusictheory.com/
* http://openmusictheory.com/scales.html
* https://www.engadget.com/2007-03-08-midi-is-the-future-of-game-audio.html
* https://voces8.foundation/si-le-le-sheet-music
* https://services.math.duke.edu/education/ccp/materials/postcalc/music/music2_4.html
* https://virtualpiano.net/
* https://music.stanford.edu/
* http://kern.ccarh.org/browse?l=beethoven/sonatas
* http://extras.humdrum.org/man/keycor/
* http://extras.humdrum.org/man/mkeyscape/
* http://extras.humdrum.org/man/mkeyscape/beet-quartet/
* https://www.qmul.ac.uk/dmrn/dmrn15/
* https://openai.com/blog/musenet/
* https://openai.com/blog/jukebox/
* https://magenta.tensorflow.org/
* https://www.acs.psu.edu/drussell/demos/waves/wavemotion.html
* https://nii-yamagishilab.github.io/samples-nsf/neural-music.html
