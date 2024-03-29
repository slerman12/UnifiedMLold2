from Sweeps.Templates import template


# Note: norm may have not worked because "low" was set to "low" not "low_" in classify
runs = template('XRD')

runs.XRD.sweep = [
    # # Mix-Soup, No-Pool-CNN
    # """task=classify/custom
    # Dataset=XRD.XRD
    # Aug=Identity
    # Trunk=Identity
    # Eyes=XRD.NoPoolCNN
    # Predictor=XRD.Predictor
    # batch_size=256
    # standardize=false
    # norm=true
    # task_name='Mix-Soup_${dataset.num_classes}-Way'
    # experiment='No-Pool-CNN'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0.5]'
    # +dataset.num_classes=7,230
    # train_steps=5e5
    # save=true
    # logger.wandb=true
    # lab=true
    # parallel=true
    # num_gpus=8
    # mem=180""",

    # # Large + RRUFF, No-Pool-CNN
    # """task=classify/custom
    # Dataset=XRD.XRD
    # Aug=Identity
    # Trunk=Identity
    # Eyes=XRD.NoPoolCNN
    # Predictor=XRD.Predictor
    # batch_size=256
    # standardize=false
    # norm=true
    # task_name='Large-and-RRUFF_${dataset.num_classes}-Way'
    # experiment='No-Pool-CNN'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 1, 0]'
    # +dataset.num_classes=7,230
    # train_steps=5e5
    # save=true
    # logger.wandb=true
    # lab=true
    # parallel=true
    # num_gpus=8
    # mem=180""",
    #
    # # Mix + RRUFF, No-Pool-CNN
    # """task=classify/custom
    # Dataset=XRD.XRD
    # Aug=Identity
    # Trunk=Identity
    # Eyes=XRD.NoPoolCNN
    # Predictor=XRD.Predictor
    # batch_size=256
    # standardize=false
    # norm=true
    # task_name='Mix-and-RRUFF_${dataset.num_classes}-Way'
    # experiment='No-Pool-CNN'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 1, 0]'
    # +dataset.num_classes=7,230
    # train_steps=5e5
    # save=true
    # logger.wandb=true
    # lab=true
    # parallel=true
    # num_gpus=8
    # mem=180""",
    #
    # # Large + RRUFF, CNN
    # """task=classify/custom
    # Dataset=XRD.XRD
    # Aug=Identity
    # Trunk=Identity
    # Eyes=XRD.NoPoolCNN
    # Predictor=XRD.Predictor
    # batch_size=256
    # standardize=false
    # norm=true
    # task_name='Large-and-RRUFF_${dataset.num_classes}-Way'
    # experiment='CNN'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 1, 0]'
    # +dataset.num_classes=7,230
    # train_steps=5e5
    # save=true
    # logger.wandb=true
    # lab=true
    # parallel=true
    # num_gpus=8
    # mem=180""",
    #
    # # Mix + RRUFF, CNN
    # """task=classify/custom
    # Dataset=XRD.XRD
    # Aug=Identity
    # Trunk=Identity
    # Eyes=XRD.CNN
    # Predictor=XRD.Predictor
    # batch_size=256
    # standardize=false
    # norm=true
    # task_name='Mix-and-RRUFF_${dataset.num_classes}-Way'
    # experiment='CNN'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 1, 0]'
    # +dataset.num_classes=7,230
    # train_steps=5e5
    # save=true
    # logger.wandb=true
    # lab=true
    # parallel=true
    # num_gpus=8
    # mem=180""",

    # # Mix-Soup, CNN
    # """task=classify/custom
    # Dataset=XRD.XRD
    # Aug=Identity
    # Trunk=Identity
    # Eyes=XRD.CNN
    # Predictor=XRD.Predictor
    # batch_size=256
    # standardize=false
    # norm=true
    # task_name='Mix-Soup_${dataset.num_classes}-Way'
    # experiment='CNN'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0.5]'
    # +dataset.num_classes=7,230
    # train_steps=5e5
    # save=true
    # logger.wandb=true
    # lab=true
    # num_workers=1
    # parallel=true
    # num_gpus=8
    # mem=180""",
    #
    # # Mix-Soup, MLP
    # """task=classify/custom
    # Dataset=XRD.XRD
    # Aug=Identity
    # Trunk=Identity
    # Eyes=Identity
    # Predictor=XRD.MLP
    # batch_size=256
    # standardize=false
    # norm=true
    # task_name='Mix-Soup_${dataset.num_classes}-Way'
    # experiment='MLP'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0.5]'
    # +dataset.num_classes=7,230
    # train_steps=5e5
    # save=true
    # logger.wandb=true
    # lab=true
    # num_workers=1
    # parallel=true
    # num_gpus=8
    # mem=180""",

    # Large-Soup, No-Pool-CNN
    # """task=classify/custom
    # Dataset=XRD.XRD
    # Aug=Identity
    # Trunk=Identity
    # Eyes=XRD.NoPoolCNN
    # Predictor=XRD.Predictor
    # batch_size=256
    # standardize=false
    # norm=true
    # task_name='Large-Soup_${dataset.num_classes}-Way'
    # experiment='No-Pool-CNN'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0.5]'
    # +dataset.num_classes=7,230
    # train_steps=5e5
    # save=true
    # logger.wandb=true
    # lab=true
    # parallel=true
    # num_gpus=8
    # mem=180""",

    # # Large-Soup, CNN
    # """task=classify/custom
    # Dataset=XRD.XRD
    # Aug=Identity
    # Trunk=Identity
    # Eyes=XRD.CNN
    # Predictor=XRD.Predictor
    # batch_size=256
    # standardize=false
    # norm=true
    # task_name='Large-Soup_${dataset.num_classes}-Way'
    # experiment='CNN'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0.5]'
    # +dataset.num_classes=7,230
    # train_steps=5e5
    # save=true
    # logger.wandb=true
    # lab=true
    # num_workers=1
    # parallel=true
    # num_gpus=8
    # mem=180""",
    #
    # # Large-Soup, MLP
    # """task=classify/custom
    # Dataset=XRD.XRD
    # Aug=Identity
    # Trunk=Identity
    # Eyes=Identity
    # Predictor=XRD.MLP
    # batch_size=256
    # standardize=false
    # norm=true
    # task_name='Large-Soup_${dataset.num_classes}-Way'
    # experiment='MLP'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0.5]'
    # +dataset.num_classes=7,230
    # train_steps=5e5
    # save=true
    # logger.wandb=true
    # lab=true
    # num_workers=1
    # parallel=true
    # num_gpus=8
    # mem=180""",

    # # Mix, No-Pool-CNN
    # """task=classify/custom
    # Dataset=XRD.XRD
    # Aug=Identity
    # Trunk=Identity
    # Eyes=XRD.NoPoolCNN
    # Predictor=XRD.Predictor
    # batch_size=256
    # standardize=false
    # norm=true
    # task_name='Mix_${dataset.num_classes}-Way'
    # experiment='No-Pool-CNN'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0]'
    # +dataset.num_classes=7,230
    # train_steps=5e5
    # save=true
    # logger.wandb=true
    # lab=true
    # num_workers=1
    # parallel=true
    # num_gpus=8
    # mem=180""",

    # # Mix, CNN
    # """task=classify/custom
    # Dataset=XRD.XRD
    # Aug=Identity
    # Trunk=Identity
    # Eyes=XRD.CNN
    # Predictor=XRD.Predictor
    # batch_size=256
    # standardize=false
    # norm=true
    # task_name='Mix_${dataset.num_classes}-Way'
    # experiment='CNN'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0]'
    # +dataset.num_classes=7,230
    # train_steps=5e5
    # save=true
    # logger.wandb=true
    # lab=true
    # num_workers=1
    # parallel=true
    # num_gpus=8
    # mem=180""",
    #
    # # Mix, MLP
    # """task=classify/custom
    # Dataset=XRD.XRD
    # Aug=Identity
    # Trunk=Identity
    # Eyes=Identity
    # Predictor=XRD.MLP
    # batch_size=256
    # standardize=false
    # norm=true
    # task_name='Mix_${dataset.num_classes}-Way'
    # experiment='MLP'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0]'
    # +dataset.num_classes=7,230
    # train_steps=5e5
    # save=true
    # logger.wandb=true
    # lab=true
    # num_workers=1
    # parallel=true
    # num_gpus=8
    # mem=180""",

    # # Large, No-Pool-CNN
    # """task=classify/custom
    # Dataset=XRD.XRD
    # Aug=Identity
    # Trunk=Identity
    # Eyes=XRD.NoPoolCNN
    # Predictor=XRD.Predictor
    # batch_size=256
    # standardize=false
    # norm=true
    # task_name='Large_${dataset.num_classes}-Way'
    # experiment='No-Pool-CNN'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0]'
    # +dataset.num_classes=7,230
    # train_steps=5e5
    # save=true
    # logger.wandb=true
    # lab=true
    # num_workers=1
    # parallel=true
    # num_gpus=8
    # mem=180""",

    # # Large, CNN
    # """task=classify/custom
    # Dataset=XRD.XRD
    # Aug=Identity
    # Trunk=Identity
    # Eyes=XRD.CNN
    # Predictor=XRD.Predictor
    # batch_size=256
    # standardize=false
    # norm=true
    # task_name='Large_${dataset.num_classes}-Way'
    # experiment='CNN'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0]'
    # +dataset.num_classes=7,230
    # train_steps=5e5
    # save=true
    # logger.wandb=true
    # lab=true
    # num_workers=1
    # parallel=true
    # num_gpus=8
    # mem=180""",

    # # Large, MLP
    # """task=classify/custom
    # Dataset=XRD.XRD
    # Aug=Identity
    # Trunk=Identity
    # Eyes=Identity
    # Predictor=XRD.MLP
    # batch_size=256
    # standardize=false
    # norm=true
    # task_name='Large_${dataset.num_classes}-Way'
    # experiment='MLP'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0]'
    # +dataset.num_classes=7,230
    # train_steps=5e5
    # save=true
    # logger.wandb=true
    # lab=true
    # num_workers=1
    # parallel=true
    # num_gpus=8
    # mem=180""",

    # # PS1, CNN
    # """task=classify/custom
    # Dataset=XRD.XRD
    # Aug=Identity
    # Trunk=Identity
    # Eyes=XRD.CNN
    # Predictor=XRD.Predictor
    # batch_size=256
    # standardize=false
    # norm=true
    # task_name='PS1_${dataset.num_classes}-Way'
    # experiment='CNN'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_ps1/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0]'
    # +dataset.num_classes=7,230
    # train_steps=5e5
    # save=true
    # logger.wandb=true
    # lab=true
    # num_gpus=8
    # mem=20""",
    #
    # # PS1, MLP
    # """task=classify/custom
    # Dataset=XRD.XRD
    # Aug=Identity
    # Trunk=Identity
    # Eyes=Identity
    # Predictor=XRD.MLP
    # batch_size=256
    # standardize=false
    # norm=true
    # task_name='PS1_${dataset.num_classes}-Way'
    # experiment='MLP'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_ps1/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0]'
    # +dataset.num_classes=7,230
    # train_steps=5e5
    # save=true
    # logger.wandb=true
    # lab=true
    # num_gpus=8
    # mem=20""",
]

# Create universal replays - Note: define for Mix-Soup and Mix+RRUFF
# runs.XRD.sweep = [
#     # Mix, MLP
#     """task=classify/custom
#     Dataset=XRD.XRD
#     Aug=Identity
#     Trunk=Identity
#     Eyes=Identity
#     Predictor=XRD.MLP
#     batch_size=256
#     standardize=false
#     norm=true
#     task_name='Mix_${dataset.num_classes}-Way'
#     experiment='MLP'
#     '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
#     +'dataset.train_eval_splits=[1, 0]'
#     +dataset.num_classes=230
#     train_steps=1
#     save=false
#     logger.wandb=true
#     lab=true
#     num_workers=1
#     num_gpus=1
#     mem=180""",

#     # Large-Soup, MLP
#     """task=classify/custom
#     Dataset=XRD.XRD
#     Aug=Identity
#     Trunk=Identity
#     Eyes=Identity
#     Predictor=XRD.MLP
#     batch_size=256
#     standardize=false
#     norm=true
#     task_name='Large-Soup_${dataset.num_classes}-Way'
#     experiment='MLP'
#     '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
#     +'dataset.train_eval_splits=[1, 0.5]'
#     +dataset.num_classes=7,230
#     train_steps=1
#     save=false
#     num_workers=1
#     logger.wandb=true
#     lab=true""",

    # # Large, MLP
    # """task=classify/custom
    # Dataset=XRD.XRD
    # Aug=Identity
    # Trunk=Identity
    # Eyes=Identity
    # Predictor=XRD.MLP
    # batch_size=256
    # standardize=false
    # norm=true
    # task_name='Large_${dataset.num_classes}-Way'
    # experiment='MLP'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0]'
    # +dataset.num_classes=7,230
    # train_steps=1
    # save=false
    # num_workers=1
    # logger.wandb=true
    # lab=true""",
    #
    # # PS1, CNN
    # """task=classify/custom
    # Dataset=XRD.XRD
    # Aug=Identity
    # Trunk=Identity
    # Eyes=XRD.CNN
    # Predictor=XRD.Predictor
    # batch_size=256
    # standardize=false
    # norm=true
    # task_name='PS1_${dataset.num_classes}-Way'
    # experiment='CNN'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_ps1/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0]'
    # +dataset.num_classes=7,230
    # train_steps=1
    # save=false
    # num_workers=1
    # logger.wandb=true
    # lab=true""",
# ]

# Generalization To Magnetic Properties
runs.XRD.sweep = [
    # Large-Soup, No-Pool-CNN - Generalize To MP
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Large-Soup_${test_dataset.num_classes}-Way'
    # experiment='No-Pool-CNN_icsd'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0.5]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LegacyDatasets/mp_icsd_shen/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/No-Pool-CNN/DQNAgent/classify/Large-Soup_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",
    #
    # # Large-Soup, CNN - Generalize To MP
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Large-Soup_${test_dataset.num_classes}-Way'
    # experiment='CNN_icsd'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0.5]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LegacyDatasets/mp_icsd_shen/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/CNN/DQNAgent/classify/Large-Soup_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",
    #
    # # Large-Soup, MLP - Generalize To MP
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Large-Soup_${test_dataset.num_classes}-Way'
    # experiment='MLP_icsd'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0.5]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LegacyDatasets/mp_icsd_shen/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/MLP/DQNAgent/classify/Large-Soup_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",
    #
    # # Mix-Soup, No-Pool-CNN - Generalize To MP
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Mix-Soup_${test_dataset.num_classes}-Way'
    # experiment='No-Pool-CNN_icsd'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0.5]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LegacyDatasets/mp_icsd_shen/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/No-Pool-CNN/DQNAgent/classify/Mix-Soup_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",

    # # Large-Soup, No-Pool-CNN - Generalize To MP nonicsd
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Large-Soup_${test_dataset.num_classes}-Way'
    # experiment='No-Pool-CNN_nonicsd'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0.5]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LegacyDatasets/mp_nonicsd_shen/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/No-Pool-CNN/DQNAgent/classify/Large-Soup_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",
    #
    # # Large-Soup, CNN - Generalize To MP nonicsd
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Large-Soup_${test_dataset.num_classes}-Way'
    # experiment='CNN_nonicsd'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0.5]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LegacyDatasets/mp_nonicsd_shen/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/CNN/DQNAgent/classify/Large-Soup_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",
    #
    # # Large-Soup, MLP - Generalize To MP nonicsd
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Large-Soup_${test_dataset.num_classes}-Way'
    # experiment='MLP_nonicsd'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0.5]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LegacyDatasets/mp_nonicsd_shen/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/MLP/DQNAgent/classify/Large-Soup_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",

    # # Mix-Soup, No-Pool-CNN - Generalize To MP nonicsd
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Mix-Soup_${test_dataset.num_classes}-Way'
    # experiment='No-Pool-CNN_nonicsd'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0.5]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LegacyDatasets/mp_nonicsd_shen/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/No-Pool-CNN/DQNAgent/classify/Mix-Soup_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",

    # Mix-Soup, CNN - Generalize To MP
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Mix-Soup_${test_dataset.num_classes}-Way'
    # experiment='CNN_icsd'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0.5]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LegacyDatasets/mp_icsd_shen/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/CNN/DQNAgent/classify/Mix-Soup_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",
    #
    # # Mix-Soup, MLP - Generalize To MP
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Mix-Soup_${test_dataset.num_classes}-Way'
    # experiment='MLP_icsd'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0.5]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LegacyDatasets/mp_icsd_shen/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/MLP/DQNAgent/classify/Mix-Soup_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",

    # # Mix-Soup, CNN - Generalize To MP nonicsd
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Mix-Soup_${test_dataset.num_classes}-Way'
    # experiment='CNN_nonicsd'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0.5]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LegacyDatasets/mp_nonicsd_shen/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/CNN/DQNAgent/classify/Mix-Soup_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",
    #
    # # Mix-Soup, MLP - Generalize To MP nonicsd
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Mix-Soup_${test_dataset.num_classes}-Way'
    # experiment='MLP_nonicsd'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0.5]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LegacyDatasets/mp_nonicsd_shen/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/MLP/DQNAgent/classify/Mix-Soup_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",

    # Large, No-Pool-CNN - Generalize To MP
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Large_${test_dataset.num_classes}-Way'
    # experiment='No-Pool-CNN_icsd'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LegacyDatasets/mp_icsd_shen/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/No-Pool-CNN/DQNAgent/classify/Large_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",
    #
    # # Large, CNN - Generalize To MP
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Large_${test_dataset.num_classes}-Way'
    # experiment='CNN_icsd'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LegacyDatasets/mp_icsd_shen/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/CNN/DQNAgent/classify/Large_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",
    #
    # # Large, MLP - Generalize To MP
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Large_${test_dataset.num_classes}-Way'
    # experiment='MLP_icsd'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LegacyDatasets/mp_icsd_shen/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/MLP/DQNAgent/classify/Large_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",

    # # Large, No-Pool-CNN - Generalize To MP nonicsd
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Large_${test_dataset.num_classes}-Way'
    # experiment='No-Pool-CNN_nonicsd'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LegacyDatasets/mp_nonicsd_shen/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/No-Pool-CNN/DQNAgent/classify/Large_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",
    #
    # # Large, CNN - Generalize To MP nonicsd
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Large_${test_dataset.num_classes}-Way'
    # experiment='CNN_nonicsd'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LegacyDatasets/mp_nonicsd_shen/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/CNN/DQNAgent/classify/Large_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",
    #
    # # Large, MLP - Generalize To MP nonicsd
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Large_${test_dataset.num_classes}-Way'
    # experiment='MLP_nonicsd'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LegacyDatasets/mp_nonicsd_shen/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/MLP/DQNAgent/classify/Large_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",

    # Mix, No-Pool-CNN - Generalize To MP - Note: Haven't trained the base model
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Mix_${test_dataset.num_classes}-Way'
    # experiment='No-Pool-CNN_icsd'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LegacyDatasets/mp_icsd_shen/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/No-Pool-CNN/DQNAgent/classify/Mix_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",
    #
    # # Mix, CNN - Generalize To MP
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Mix_${test_dataset.num_classes}-Way'
    # experiment='CNN_icsd'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LegacyDatasets/mp_icsd_shen/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/CNN/DQNAgent/classify/Mix_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",
    #
    # # Mix, MLP - Generalize To MP
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Mix_${test_dataset.num_classes}-Way'
    # experiment='MLP_icsd'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LegacyDatasets/mp_icsd_shen/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/MLP/DQNAgent/classify/Mix_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",

    # Mix, No-Pool-CNN - Generalize To MP nonicsd - Note: Haven't trained the base model
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Mix_${test_dataset.num_classes}-Way'
    # experiment='No-Pool-CNN_nonicsd'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LegacyDatasets/mp_nonicsd_shen/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/No-Pool-CNN/DQNAgent/classify/Mix_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",
    #
    # # Mix, CNN - Generalize To MP nonicsd
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Mix_${test_dataset.num_classes}-Way'
    # experiment='CNN_nonicsd'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LegacyDatasets/mp_nonicsd_shen/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/CNN/DQNAgent/classify/Mix_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",
    #
    # # Mix, MLP - Generalize To MP nonicsd
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Mix_${test_dataset.num_classes}-Way'
    # experiment='MLP_nonicsd'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LegacyDatasets/mp_nonicsd_shen/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/MLP/DQNAgent/classify/Mix_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",
]


# Generalization To Magnetic Properties & LATT
runs.XRD.sweep = [
    # Large-Soup, No-Pool-CNN - Generalize To MP
    """task=classify/custom
    Dataset=XRD.XRD
    batch_size=256
    task_name='Large-Soup_${test_dataset.num_classes}-Way'
    experiment='No-Pool-CNN_MP'
    '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    +'dataset.train_eval_splits=[1, 0.5]'
    '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/mp_shen/"]'
    +'test_dataset.train_eval_splits=[0]'
    +test_dataset.num_classes=7,230
    TestDataset=XRD.XRD
    train_steps=0
    load=true
    load_path='/scratch/slerman/UnifiedML/Checkpoints/No-Pool-CNN/DQNAgent/classify/Large-Soup_${test_dataset.num_classes}-Way_1.pt'
    logger.wandb=true
    num_workers=8
    num_gpus=8
    lab=true
    save=false
    parallel=true
    mem=180""",

    # Large-Soup, CNN - Generalize To MP
    """task=classify/custom
    Dataset=XRD.XRD
    batch_size=256
    task_name='Large-Soup_${test_dataset.num_classes}-Way'
    experiment='CNN_MP'
    '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    +'dataset.train_eval_splits=[1, 0.5]'
    '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/mp_shen/"]'
    +'test_dataset.train_eval_splits=[0]'
    +test_dataset.num_classes=7,230
    TestDataset=XRD.XRD
    train_steps=0
    load=true
    load_path='/scratch/slerman/UnifiedML/Checkpoints/CNN/DQNAgent/classify/Large-Soup_${test_dataset.num_classes}-Way_1.pt'
    logger.wandb=true
    num_workers=8
    num_gpus=8
    lab=true
    save=false
    parallel=true
    mem=180""",

    # Large-Soup, MLP - Generalize To MP
    """task=classify/custom
    Dataset=XRD.XRD
    batch_size=256
    task_name='Large-Soup_${test_dataset.num_classes}-Way'
    experiment='MLP_MP'
    '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    +'dataset.train_eval_splits=[1, 0.5]'
    '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/mp_shen/"]'
    +'test_dataset.train_eval_splits=[0]'
    +test_dataset.num_classes=7,230
    TestDataset=XRD.XRD
    train_steps=0
    load=true
    load_path='/scratch/slerman/UnifiedML/Checkpoints/MLP/DQNAgent/classify/Large-Soup_${test_dataset.num_classes}-Way_1.pt'
    logger.wandb=true
    num_workers=8
    num_gpus=8
    lab=true
    save=false
    parallel=true
    mem=180""",

    # Mix-Soup, No-Pool-CNN - Generalize To MP
    """task=classify/custom
    Dataset=XRD.XRD
    batch_size=256
    task_name='Mix-Soup_${test_dataset.num_classes}-Way'
    experiment='No-Pool-CNN_MP'
    '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    +'dataset.train_eval_splits=[1, 0.5]'
    '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/mp_shen/"]'
    +'test_dataset.train_eval_splits=[0]'
    +test_dataset.num_classes=7,230
    TestDataset=XRD.XRD
    train_steps=0
    load=true
    load_path='/scratch/slerman/UnifiedML/Checkpoints/No-Pool-CNN/DQNAgent/classify/Mix-Soup_${test_dataset.num_classes}-Way_1.pt'
    logger.wandb=true
    num_workers=8
    num_gpus=8
    lab=true
    save=false
    parallel=true
    mem=180""",

    # # Large-Soup, No-Pool-CNN - Generalize To LATT
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Large-Soup_${test_dataset.num_classes}-Way'
    # experiment='No-Pool-CNN_LATT'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0.5]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LATT/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/No-Pool-CNN/DQNAgent/classify/Large-Soup_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",

    # # Large-Soup, CNN - Generalize To LATT
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Large-Soup_${test_dataset.num_classes}-Way'
    # experiment='CNN_LATT'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0.5]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LATT/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/CNN/DQNAgent/classify/Large-Soup_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",

    # # Large-Soup, MLP - Generalize To LATT
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Large-Soup_${test_dataset.num_classes}-Way'
    # experiment='MLP_LATT'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0.5]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LATT/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/MLP/DQNAgent/classify/Large-Soup_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",

    # # Mix-Soup, No-Pool-CNN - Generalize To LATT
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Mix-Soup_${test_dataset.num_classes}-Way'
    # experiment='No-Pool-CNN_LATT'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0.5]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LATT/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/No-Pool-CNN/DQNAgent/classify/Mix-Soup_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",

    # Mix-Soup, CNN - Generalize To MP
    """task=classify/custom
    Dataset=XRD.XRD
    batch_size=256
    task_name='Mix-Soup_${test_dataset.num_classes}-Way'
    experiment='CNN_MP'
    '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    +'dataset.train_eval_splits=[1, 0.5]'
    '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/mp_shen/"]'
    +'test_dataset.train_eval_splits=[0]'
    +test_dataset.num_classes=7,230
    TestDataset=XRD.XRD
    train_steps=0
    load=true
    load_path='/scratch/slerman/UnifiedML/Checkpoints/CNN/DQNAgent/classify/Mix-Soup_${test_dataset.num_classes}-Way_1.pt'
    logger.wandb=true
    num_workers=8
    num_gpus=8
    lab=true
    save=false
    parallel=true
    mem=180""",

    # Mix-Soup, MLP - Generalize To MP
    """task=classify/custom
    Dataset=XRD.XRD
    batch_size=256
    task_name='Mix-Soup_${test_dataset.num_classes}-Way'
    experiment='MLP_MP'
    '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    +'dataset.train_eval_splits=[1, 0.5]'
    '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/mp_shen/"]'
    +'test_dataset.train_eval_splits=[0]'
    +test_dataset.num_classes=7,230
    TestDataset=XRD.XRD
    train_steps=0
    load=true
    load_path='/scratch/slerman/UnifiedML/Checkpoints/MLP/DQNAgent/classify/Mix-Soup_${test_dataset.num_classes}-Way_1.pt'
    logger.wandb=true
    num_workers=8
    num_gpus=8
    lab=true
    save=false
    parallel=true
    mem=180""",

    # # Mix-Soup, CNN - Generalize To LATT
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Mix-Soup_${test_dataset.num_classes}-Way'
    # experiment='CNN_LATT'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0.5]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LATT/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/CNN/DQNAgent/classify/Mix-Soup_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",

    # # Mix-Soup, MLP - Generalize To LATT
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Mix-Soup_${test_dataset.num_classes}-Way'
    # experiment='MLP_LATT'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0.5]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LATT/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/MLP/DQNAgent/classify/Mix-Soup_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",

    # Large, No-Pool-CNN - Generalize To MP
    """task=classify/custom
    Dataset=XRD.XRD
    batch_size=256
    task_name='Large_${test_dataset.num_classes}-Way'
    experiment='No-Pool-CNN_MP'
    '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    +'dataset.train_eval_splits=[1, 0]'
    '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/mp_shen/"]'
    +'test_dataset.train_eval_splits=[0]'
    +test_dataset.num_classes=7,230
    TestDataset=XRD.XRD
    train_steps=0
    load=true
    load_path='/scratch/slerman/UnifiedML/Checkpoints/No-Pool-CNN/DQNAgent/classify/Large_${test_dataset.num_classes}-Way_1.pt'
    logger.wandb=true
    num_workers=8
    num_gpus=8
    lab=true
    save=false
    parallel=true
    mem=180""",

    # Large, CNN - Generalize To MP
    """task=classify/custom
    Dataset=XRD.XRD
    batch_size=256
    task_name='Large_${test_dataset.num_classes}-Way'
    experiment='CNN_MP'
    '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    +'dataset.train_eval_splits=[1, 0]'
    '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/mp_shen/"]'
    +'test_dataset.train_eval_splits=[0]'
    +test_dataset.num_classes=7,230
    TestDataset=XRD.XRD
    train_steps=0
    load=true
    load_path='/scratch/slerman/UnifiedML/Checkpoints/CNN/DQNAgent/classify/Large_${test_dataset.num_classes}-Way_1.pt'
    logger.wandb=true
    num_workers=8
    num_gpus=8
    lab=true
    save=false
    parallel=true
    mem=180""",

    # Large, MLP - Generalize To MP
    """task=classify/custom
    Dataset=XRD.XRD
    batch_size=256
    task_name='Large_${test_dataset.num_classes}-Way'
    experiment='MLP_MP'
    '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    +'dataset.train_eval_splits=[1, 0]'
    '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/mp_shen/"]'
    +'test_dataset.train_eval_splits=[0]'
    +test_dataset.num_classes=7,230
    TestDataset=XRD.XRD
    train_steps=0
    load=true
    load_path='/scratch/slerman/UnifiedML/Checkpoints/MLP/DQNAgent/classify/Large_${test_dataset.num_classes}-Way_1.pt'
    logger.wandb=true
    num_workers=8
    num_gpus=8
    lab=true
    save=false
    parallel=true
    mem=180""",

    # # Large, No-Pool-CNN - Generalize To LATT
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Large_${test_dataset.num_classes}-Way'
    # experiment='No-Pool-CNN_LATT'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LATT/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/No-Pool-CNN/DQNAgent/classify/Large_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",

    # # Large, CNN - Generalize To LATT
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Large_${test_dataset.num_classes}-Way'
    # experiment='CNN_LATT'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LATT/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/CNN/DQNAgent/classify/Large_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",

    # # Large, MLP - Generalize To LATT
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Large_${test_dataset.num_classes}-Way'
    # experiment='MLP_LATT'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LATT/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/MLP/DQNAgent/classify/Large_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",

    # Mix, No-Pool-CNN - Generalize To MP - Note: Haven't trained the base model
    """task=classify/custom
    Dataset=XRD.XRD
    batch_size=256
    task_name='Mix_${test_dataset.num_classes}-Way'
    experiment='No-Pool-CNN_MP'
    '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    +'dataset.train_eval_splits=[1, 0]'
    '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/mp_shen/"]'
    +'test_dataset.train_eval_splits=[0]'
    +test_dataset.num_classes=7,230
    TestDataset=XRD.XRD
    train_steps=0
    load=true
    load_path='/scratch/slerman/UnifiedML/Checkpoints/No-Pool-CNN/DQNAgent/classify/Mix_${test_dataset.num_classes}-Way_1.pt'
    logger.wandb=true
    num_workers=8
    num_gpus=8
    lab=true
    save=false
    parallel=true
    mem=180""",

    # Mix, CNN - Generalize To MP
    """task=classify/custom
    Dataset=XRD.XRD
    batch_size=256
    task_name='Mix_${test_dataset.num_classes}-Way'
    experiment='CNN_MP'
    '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    +'dataset.train_eval_splits=[1, 0]'
    '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/mp_shen/"]'
    +'test_dataset.train_eval_splits=[0]'
    +test_dataset.num_classes=7,230
    TestDataset=XRD.XRD
    train_steps=0
    load=true
    load_path='/scratch/slerman/UnifiedML/Checkpoints/CNN/DQNAgent/classify/Mix_${test_dataset.num_classes}-Way_1.pt'
    logger.wandb=true
    num_workers=8
    num_gpus=8
    lab=true
    save=false
    parallel=true
    mem=180""",

    # Mix, MLP - Generalize To MP
    """task=classify/custom
    Dataset=XRD.XRD
    batch_size=256
    task_name='Mix_${test_dataset.num_classes}-Way'
    experiment='MLP_MP'
    '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    +'dataset.train_eval_splits=[1, 0]'
    '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/mp_shen/"]'
    +'test_dataset.train_eval_splits=[0]'
    +test_dataset.num_classes=7,230
    TestDataset=XRD.XRD
    train_steps=0
    load=true
    load_path='/scratch/slerman/UnifiedML/Checkpoints/MLP/DQNAgent/classify/Mix_${test_dataset.num_classes}-Way_1.pt'
    logger.wandb=true
    num_workers=8
    num_gpus=8
    lab=true
    save=false
    parallel=true
    mem=180""",

    # # Mix, No-Pool-CNN - Generalize To LATT - Note: Haven't trained the base model
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Mix_${test_dataset.num_classes}-Way'
    # experiment='No-Pool-CNN_LATT'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LATT/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/No-Pool-CNN/DQNAgent/classify/Mix_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",

    # # Mix, CNN - Generalize To LATT
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Mix_${test_dataset.num_classes}-Way'
    # experiment='CNN_LATT'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LATT/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/CNN/DQNAgent/classify/Mix_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",

    # # Mix, MLP - Generalize To LATT
    # """task=classify/custom
    # Dataset=XRD.XRD
    # batch_size=256
    # task_name='Mix_${test_dataset.num_classes}-Way'
    # experiment='MLP_LATT'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0]'
    # '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LATT/"]'
    # +'test_dataset.train_eval_splits=[0]'
    # +test_dataset.num_classes=7,230
    # TestDataset=XRD.XRD
    # train_steps=0
    # load=true
    # load_path='/scratch/slerman/UnifiedML/Checkpoints/MLP/DQNAgent/classify/Mix_${test_dataset.num_classes}-Way_1.pt'
    # logger.wandb=true
    # num_workers=8
    # num_gpus=8
    # lab=true
    # save=false
    # parallel=true
    # mem=180""",
]

# TEst
runs.XRD.sweep = [
    # Mix, MLP - Generalize To MP
    """task=classify/custom
    Dataset=XRD.XRD
    batch_size=256
    task_name='Mix_${test_dataset.num_classes}-Way'
    experiment='MLP_MP'
    '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    +'dataset.train_eval_splits=[1, 0]'
    '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/mp_shen/"]'
    +'test_dataset.train_eval_splits=[0]'
    +test_dataset.num_classes=7,230
    TestDataset=XRD.XRD
    train_steps=0
    load=true
    load_path='/scratch/slerman/UnifiedML/Checkpoints/MLP/DQNAgent/classify/Mix_${test_dataset.num_classes}-Way_1.pt'
    logger.wandb=true
    num_workers=8
    num_gpus=8
    lab=true
    save=false
    parallel=true
    mem=180""",
]

# # Just a test
# runs.XRD.sweep = [# # Mix, MLP - Generalize To MP nonicsd
#     """task=classify/custom
#     Dataset=XRD.XRD
#     batch_size=256
#     task_name='Mix_${test_dataset.num_classes}-Way'
#     experiment='MLP_nonicsd'
#     '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
#     +'dataset.train_eval_splits=[1, 0]'
#     '+test_dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/LegacyDatasets/mp_nonicsd_shen/"]'
#     +'test_dataset.train_eval_splits=[0]'
#     +test_dataset.num_classes=7
#     TestDataset=XRD.XRD
#     train_steps=0
#     load=true
#     load_path='/scratch/slerman/UnifiedML/Checkpoints/MLP/DQNAgent/classify/Mix_${test_dataset.num_classes}-Way_1.pt'
#     logger.wandb=true
#     num_workers=8
#     num_gpus=8
#     lab=true
#     save=false
#     parallel=true
#     mem=180""",
# ]

# Re-evaluate with "Predicted vs. Actual"
# runs.XRD.sweep = [
    # # Mix-Soup, No-Pool-CNN
    # """task=classify/custom
    # Dataset=XRD.XRD
    # Aug=Identity
    # Trunk=Identity
    # Eyes=XRD.NoPoolCNN
    # Predictor=XRD.Predictor
    # batch_size=256
    # standardize=false
    # norm=true
    # task_name='Mix-Soup_${dataset.num_classes}-Way'
    # experiment='No-Pool-CNN'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0.5]'
    # +dataset.num_classes=7,230
    # load=true
    # train_steps=0
    # save=true
    # logger.wandb=true
    # lab=true
    # parallel=true
    # num_gpus=8
    # mem=180""",
    #
    # # Large + RRUFF, No-Pool-CNN
    # """task=classify/custom
    # Dataset=XRD.XRD
    # Aug=Identity
    # Trunk=Identity
    # Eyes=XRD.NoPoolCNN
    # Predictor=XRD.Predictor
    # batch_size=256
    # standardize=false
    # norm=true
    # task_name='Large-and-RRUFF_${dataset.num_classes}-Way'
    # experiment='No-Pool-CNN'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 1, 0]'
    # +dataset.num_classes=7,230
    # load=true
    # train_steps=0
    # save=true
    # logger.wandb=true
    # lab=true
    # parallel=true
    # num_gpus=8
    # mem=180""",
    #
    # # Mix + RRUFF, No-Pool-CNN
    # """task=classify/custom
    # Dataset=XRD.XRD
    # Aug=Identity
    # Trunk=Identity
    # Eyes=XRD.NoPoolCNN
    # Predictor=XRD.Predictor
    # batch_size=256
    # standardize=false
    # norm=true
    # task_name='Mix-and-RRUFF_${dataset.num_classes}-Way'
    # experiment='No-Pool-CNN'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 1, 0]'
    # +dataset.num_classes=7,230
    # load=true
    # train_steps=0
    # save=true
    # logger.wandb=true
    # lab=true
    # parallel=true
    # num_gpus=8
    # mem=180""",
    #
    # # Large + RRUFF, CNN
    # """task=classify/custom
    # Dataset=XRD.XRD
    # Aug=Identity
    # Trunk=Identity
    # Eyes=XRD.NoPoolCNN
    # Predictor=XRD.Predictor
    # batch_size=256
    # standardize=false
    # norm=true
    # task_name='Large-and-RRUFF_${dataset.num_classes}-Way'
    # experiment='CNN'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 1, 0]'
    # +dataset.num_classes=7,230
    # load=true
    # train_steps=0
    # save=true
    # logger.wandb=true
    # lab=true
    # parallel=true
    # num_gpus=8
    # mem=180""",
    #
    # # Mix + RRUFF, CNN
    # """task=classify/custom
    # Dataset=XRD.XRD
    # Aug=Identity
    # Trunk=Identity
    # Eyes=XRD.CNN
    # Predictor=XRD.Predictor
    # batch_size=256
    # standardize=false
    # norm=true
    # task_name='Mix-and-RRUFF_${dataset.num_classes}-Way'
    # experiment='CNN'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 1, 0]'
    # +dataset.num_classes=7,230
    # load=true
    # train_steps=0
    # save=true
    # logger.wandb=true
    # lab=true
    # parallel=true
    # num_gpus=8
    # mem=180""",
    #
    # # Mix-Soup, CNN
    # """task=classify/custom
    # Dataset=XRD.XRD
    # Aug=Identity
    # Trunk=Identity
    # Eyes=XRD.CNN
    # Predictor=XRD.Predictor
    # batch_size=256
    # standardize=false
    # norm=true
    # task_name='Mix-Soup_${dataset.num_classes}-Way'
    # experiment='CNN'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0.5]'
    # +dataset.num_classes=7,230
    # load=true
    # train_steps=0
    # save=true
    # logger.wandb=true
    # lab=true
    # num_workers=1
    # parallel=true
    # num_gpus=8
    # mem=180""",
    #
    # # Mix-Soup, MLP
    # """task=classify/custom
    # Dataset=XRD.XRD
    # Aug=Identity
    # Trunk=Identity
    # Eyes=Identity
    # Predictor=XRD.MLP
    # batch_size=256
    # standardize=false
    # norm=true
    # task_name='Mix-Soup_${dataset.num_classes}-Way'
    # experiment='MLP'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0.5]'
    # +dataset.num_classes=7,230
    # load=true
    # train_steps=0
    # save=true
    # logger.wandb=true
    # lab=true
    # num_workers=1
    # parallel=true
    # num_gpus=8
    # mem=180""",

    # # Large-Soup, No-Pool-CNN
    # """task=classify/custom
    # Dataset=XRD.XRD
    # Aug=Identity
    # Trunk=Identity
    # Eyes=XRD.NoPoolCNN
    # Predictor=XRD.Predictor
    # batch_size=256
    # standardize=false
    # norm=true
    # task_name='Large-Soup_${dataset.num_classes}-Way'
    # experiment='No-Pool-CNN'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0.5]'
    # +dataset.num_classes=7,230
    # load=true
    # train_steps=0
    # save=true
    # logger.wandb=true
    # lab=true
    # parallel=true
    # num_gpus=8
    # mem=180""",
    #
    # # Large-Soup, CNN
    # """task=classify/custom
    # Dataset=XRD.XRD
    # Aug=Identity
    # Trunk=Identity
    # Eyes=XRD.CNN
    # Predictor=XRD.Predictor
    # batch_size=256
    # standardize=false
    # norm=true
    # task_name='Large-Soup_${dataset.num_classes}-Way'
    # experiment='CNN'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0.5]'
    # +dataset.num_classes=7,230
    # load=true
    # train_steps=0
    # save=true
    # logger.wandb=true
    # lab=true
    # num_workers=1
    # parallel=true
    # num_gpus=8
    # mem=180""",
    #
    # # Large-Soup, MLP
    # """task=classify/custom
    # Dataset=XRD.XRD
    # Aug=Identity
    # Trunk=Identity
    # Eyes=Identity
    # Predictor=XRD.MLP
    # batch_size=256
    # standardize=false
    # norm=true
    # task_name='Large-Soup_${dataset.num_classes}-Way'
    # experiment='MLP'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0.5]'
    # +dataset.num_classes=7,230
    # load=true
    # train_steps=0
    # save=true
    # logger.wandb=true
    # lab=true
    # num_workers=1
    # parallel=true
    # num_gpus=8
    # mem=180""",
    #
    # # Mix, No-Pool-CNN
    # """task=classify/custom
    # Dataset=XRD.XRD
    # Aug=Identity
    # Trunk=Identity
    # Eyes=XRD.NoPoolCNN
    # Predictor=XRD.Predictor
    # batch_size=256
    # standardize=false
    # norm=true
    # task_name='Mix_${dataset.num_classes}-Way'
    # experiment='No-Pool-CNN'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0]'
    # +dataset.num_classes=7,230
    # load=true
    # train_steps=0
    # save=true
    # logger.wandb=true
    # lab=true
    # num_workers=1
    # parallel=true
    # num_gpus=8
    # mem=180""",
    #
    # # Mix, CNN
    # """task=classify/custom
    # Dataset=XRD.XRD
    # Aug=Identity
    # Trunk=Identity
    # Eyes=XRD.CNN
    # Predictor=XRD.Predictor
    # batch_size=256
    # standardize=false
    # norm=true
    # task_name='Mix_${dataset.num_classes}-Way'
    # experiment='CNN'
    # '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
    # +'dataset.train_eval_splits=[1, 0]'
    # +dataset.num_classes=7,230
    # load=true
    # train_steps=0
    # save=true
    # logger.wandb=true
    # lab=true
    # num_workers=1
    # parallel=true
    # num_gpus=8
    # mem=180""",
    #
    # Mix, MLP
#     """task=classify/custom
#     Dataset=XRD.XRD
#     Aug=Identity
#     Trunk=Identity
#     Eyes=Identity
#     Predictor=XRD.MLP
#     batch_size=256
#     standardize=false
#     norm=true
#     task_name='Mix_${dataset.num_classes}-Way'
#     experiment='MLP'
#     '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_mix/icsd171k_mix/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
#     +'dataset.train_eval_splits=[1, 0]'
#     +dataset.num_classes=7,230
#     load=true
#     train_steps=0
#     save=true
#     logger.wandb=true
#     lab=true
#     num_workers=1
#     parallel=true
#     num_gpus=8
#     mem=180""",
#
#     # Large, No-Pool-CNN
#     """task=classify/custom
#     Dataset=XRD.XRD
#     Aug=Identity
#     Trunk=Identity
#     Eyes=XRD.NoPoolCNN
#     Predictor=XRD.Predictor
#     batch_size=256
#     standardize=false
#     norm=true
#     task_name='Large_${dataset.num_classes}-Way'
#     experiment='No-Pool-CNN'
#     '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
#     +'dataset.train_eval_splits=[1, 0]'
#     +dataset.num_classes=7,230
#     load=true
#     train_steps=0
#     save=true
#     logger.wandb=true
#     lab=true
#     num_workers=1
#     parallel=true
#     num_gpus=8
#     mem=180""",
#
#     # Large, CNN
#     """task=classify/custom
#     Dataset=XRD.XRD
#     Aug=Identity
#     Trunk=Identity
#     Eyes=XRD.CNN
#     Predictor=XRD.Predictor
#     batch_size=256
#     standardize=false
#     norm=true
#     task_name='Large_${dataset.num_classes}-Way'
#     experiment='CNN'
#     '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
#     +'dataset.train_eval_splits=[1, 0]'
#     +dataset.num_classes=7,230
#     load=true
#     train_steps=0
#     save=true
#     logger.wandb=true
#     lab=true
#     num_workers=1
#     parallel=true
#     num_gpus=8
#     mem=180""",
#
#     # Large, MLP
#     """task=classify/custom
#     Dataset=XRD.XRD
#     Aug=Identity
#     Trunk=Identity
#     Eyes=Identity
#     Predictor=XRD.MLP
#     batch_size=256
#     standardize=false
#     norm=true
#     task_name='Large_${dataset.num_classes}-Way'
#     experiment='MLP'
#     '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd1.2m_large/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
#     +'dataset.train_eval_splits=[1, 0]'
#     +dataset.num_classes=7,230
#     load=true
#     train_steps=0
#     save=true
#     logger.wandb=true
#     lab=true
#     num_workers=1
#     parallel=true
#     num_gpus=8
#     mem=180""",
#
#     # PS1, CNN
#     """task=classify/custom
#     Dataset=XRD.XRD
#     Aug=Identity
#     Trunk=Identity
#     Eyes=XRD.CNN
#     Predictor=XRD.Predictor
#     batch_size=256
#     standardize=false
#     norm=true
#     task_name='PS1_${dataset.num_classes}-Way'
#     experiment='CNN'
#     '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_ps1/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
#     +'dataset.train_eval_splits=[1, 0]'
#     +dataset.num_classes=7,230
#     load=true
#     train_steps=0
#     save=true
#     logger.wandb=true
#     lab=true
#     num_gpus=8
#     mem=20""",
#
#     # PS1, MLP
#     """task=classify/custom
#     Dataset=XRD.XRD
#     Aug=Identity
#     Trunk=Identity
#     Eyes=Identity
#     Predictor=XRD.MLP
#     batch_size=256
#     standardize=false
#     norm=true
#     task_name='PS1_${dataset.num_classes}-Way'
#     experiment='MLP'
#     '+dataset.roots=["/gpfs/fs2/scratch/public/jsalgad2/icsd171k_ps1/","/scratch/slerman/XRDs/icsd_Datasets/rruff/XY_DIF_noiseAll/"]'
#     +'dataset.train_eval_splits=[1, 0]'
#     +dataset.num_classes=7,230
#     load=true
#     train_steps=0
#     save=true
#     logger.wandb=true
#     lab=true
#     num_gpus=8
#     mem=20""",
#
# ]

# Original Summary
# runs.XRD.plots = [
#     ['CNN_optim.*', 'MLP_optim_.*'],
# ]
# runs.XRD.tasks = [
#     'Soup-50-50.*', 'Synthetic.*'
# ]

# For Suites Aggregation
# runs.XRD.plots = [
#     ['CNN', 'MLP', 'No-Pool-CNN'],
# ]
# runs.XRD.tasks = [
#     'Large.*', 'Mix-Soup.*'
# ]

# runs.XRD.plots = [
#     ['CNN', 'MLP', 'No-Pool-CNN'],
# ]
# runs.XRD.tasks = [
#     'PS1_.*', 'Large_.*', 'Mix_.*', 'Large-Soup_.*', 'Mix-Soup_.*'
# ]
# runs.XRD.tasks = [
#     'Large-Soup_.*'
# ]

# runs.XRD.title = 'RRUFF'

runs.XRD.plots = [
    # ['.*icsd.*'],
    # ['.*_icsd.*'],
    # ['.*_nonicsd.*'],
    ['.*MP'],
    # ['.*LATT']
]

runs.XRD.title = 'Magnetic Properties'
runs.XRD.sftp = False
