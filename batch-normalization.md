# Batch Normalization 学习笔记

## Introduction
       
训练深度神经网络的复杂性在于，每层输入的分布在训练过程中会发生变化，因为前面的层的参数会发生变化。通过要求较低的学习率和仔细的参数初始化减慢了训练，并且使具有饱和非线性（sigmoid）的模型训练起来非常困难。我们将这种现象称为 _内部协变量转移_ ，并通过标准化层输入来解决这个问题。我们的方法力图使 normalization 成为模型架构的一部分，并为每小批量数据执行Normalization。_Batch Normalization_ 使我们能够使用更高的学习率，并且不用太注意初始化。它也作为一个正则化项，在某些情况将下不需要 _Dropout_。将 _Batch Normalization_ 应用到最先进的图像分类模型上，在取得相同的精度的情况下，减少了14倍的训练步骤，并以显著的差距击败了原始模型。使用批标准化网络的组合，我们改进了在ImageNet分类上公布的最佳结果：达到了4.9％ top-5的验证误差（和4.8％测试误差），超过了人类评估者的准确性
     
随后论文分析了为什么让每层输入标准化有利于整个神经网络，讲了两点：
- 由于每一层的输入都是等价的，让每一层的训练数据和测试数据之间有相同的分布（分布在时间上保持固定是有利的），会对整个训练过程有极大的贡献。
- 当使用饱和非线性单元时，输入分布的变化时常造成梯度消失或者让输出流向饱和状态，这会让整个训练过程变得很缓慢。
    
在Introduction的最后，论文谈到了，由于 _Batch Normalization_ 的正则化和稳定输入的这些效果，让放弃 _Dropout_ 和使用饱和非线性单元成为可能
      
## Towards Reducing Internal Covariate Shift
     
论文在谈到这些时，提到了两个概念：
- 白化（whitened）：用于去除数据的冗余信息。
- 主成分分析（PCA）：减少数据的维数，同时保持数据集中对方差贡献最大的特征
     
首先作者提及了LeCun等人的工作，将网络的输入进行白化（上面有解释）将会对网络训练过程产生帮助（网络会收敛的更快）。如果每一层网络都对上一层的输入进行百花操作，将在一定程度消除 _内部协变量转移_ 产生的负面影响。   

随后，作者说了一句话：
> We could consider whitening activations at every training step or at some interval, either by modifying the network directly or by changing the parametres of the optimization algorithm to depend on the network activation values.     

我不是太懂这句话的意思，可能是要看后面refer的几篇论文才可以理解，所以只能继续往后面看了。   

其实第二部分主要就是在说 _Normalization_ 时，必须要考虑操作对整体数值的影响，所以在进行梯度计算时，必须要计算 _Normalization_ 操作对梯度的影响。   

## Normalization via Mini-Batch Statistic

这里详细叙述了如何去一个 _mini-batch_ 进行训练，具体的公式和梯度计算在这里不再赘述。实际上个人感觉这里的操作与train的方法很相似，都是取一小batch的数据，让它们全部流入网络，再对它们进行一次整体的计算。   

## Test

这里有一个小trick，就是对train过程中的均值和方差进行计算，由于整个训练过程，权重在不断变化，所以越往后的均值和方差的权重越大。   

## Experiment

总结：BN算法很强
