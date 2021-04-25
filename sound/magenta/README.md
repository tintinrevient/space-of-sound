# Magenta

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

```bash
lspci
```

* https://www.tensorflow.org/api_docs/python/tf/test/is_gpu_available
* https://www.tensorflow.org/install/source#gpu
* https://www.tensorflow.org/tensorboard/get_started

## References

* https://github.com/magenta/magenta/tree/master/magenta/models/music_vae
* https://colab.research.google.com/github/magenta/magenta-demos/blob/master/colab-notebooks/MusicVAE.ipynb
* https://notebook.community/magenta/magenta-demos/colab-notebooks/MusicVAE
* http://www.vgmusic.com/
