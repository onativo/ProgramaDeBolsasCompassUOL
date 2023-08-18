# Avaliação Sprint 5 - Programa de Bolsas Compass UOL / AWS e Univesp

Avaliação da [quinta sprint][sprint5main] do programa de bolsas [Compass UOL][compass] para formação em machine learning para [AWS][aws].

***

Este é um projeto de machine learning que usa o conjunto de dados MNIST para treinar um modelo de classificação de imagens de dígitos manuscritos de 0 a 9. O modelo foi treinado usando o Amazon SageMaker.

## Conjunto de Dados MNIST
O conjunto de dados MNIST consiste em 70.000 imagens de dígitos manuscritos (0 a 9) com um tamanho de 28x28 pixels cada. O conjunto de dados é amplamente utilizado para treinar e testar algoritmos de reconhecimento de padrões e classificação de imagens. 

O conjunto MNIST pode ser importado diretamente do TensorFlow com o comando:

``` 
import tensorflow
from tensorflow.keras.datasets import mnist
```

![MNIST](https://upload.wikimedia.org/wikipedia/commons/2/27/MnistExamples.png)


## Ambiente
O projeto foi desenvolvido utilizando o ambiente AWS. Os seguintes serviços da AWS foram usados:

- Amazon SageMaker: treinamento e implantação do modelo de ML.
- Amazon S3: armazenamento do modelo treinado.


## Modelo
O modelo de ML usado neste projeto é uma Rede Neural Convolucional (CNN). A CNN foi desenvolvida usando a biblioteca Keras e treinada usando o TensorFlow. 

![model](https://www.insightlab.ufc.br/wp-content/webp-express/webp-images/doc-root/wp-content/uploads/2021/07/2.jpg.webp)

**O modelo obteve acurácia de 99,68% no conjunto de treino e 97,85% no conjunto de teste.**



## Como Executar o Projeto
- Faça o login na sua conta do Amazon SageMaker.
- Crie um novo notebook instance e selecione o tipo de instância e a imagem de ambiente que deseja usar.
- Faça download do notebook [tensorflow.ipynb](/src/tensorflow.ipynb) e execute as células de código na ordem indicada.
- Após o treinamento e teste da rede, faça download do notebook [tensorflow-sagemaker.ipynb](/src/tensorflow-sagemaker.ipynb) para salvar o modelo dentro do Bucket S3 na AWS.

## Referências
- [TensorFlow](https://www.tensorflow.org/datasets/catalog/overview?hl=pt-br)
- [MNIST](https://www.tensorflow.org/datasets/catalog/mnist?hl=pt-br)
- [CNN](https://en.wikipedia.org/wiki/Convolutional_neural_network])
- [Amazon SageMaker](https://aws.amazon.com/sagemaker/)
- [JupyterLab Notebook](https://jupyter.org/)


## Dificuldades
- Definir os parâmetros para execução da base de treinamento.
- Estrutura e funcionamento da rede treinada.

***


## Desenvolvedores do projeto
| [<img src="https://avatars.githubusercontent.com/u/25699466?v=4" width=115><br><sub>Bruno Monserrat Perillo</sub>](https://github.com/brunoperillo) | [<img src="https://avatars.githubusercontent.com/u/124359272?v=4" width=115><br><sub>Irati Gonçalves Maffra</sub>](https://github.com/IratiMaffra) | [<img src="https://avatars.githubusercontent.com/u/35769020?v=4" width=115><br><sub>Marcio Lima Brunelli</sub>](https://github.com/ml-brunelli) | [<img src="https://avatars.githubusercontent.com/u/73674662?v=4" width=115><br><sub>Marcos Vinicios Nativo de Carvalho</sub>](https://github.com/onativo) | [<img src="https://avatars.githubusercontent.com/u/94749597?v=4" width=115><br><sub>O'Dhara Maggi</sub>](https://github.com/odharamaggi) |
| :---: | :---: | :---: |:---: |:---: |


***
   [kernel]: <https://pt.wikipedia.org/wiki/N%C3%BAcleo_(sistema_operacional)>
   [compass]: <https://compass.uol/en/home/>
   [aws]: <https://aws.amazon.com/pt/>
   [sprint5main]: <https://github.com/Compass-pb-aws-2023-Univesp/sprint-5-pb-aws-univesp>
   [endpoint]: <http://54.163.32.88:9000/>
