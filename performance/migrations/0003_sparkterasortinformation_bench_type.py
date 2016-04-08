# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('performance', '0002_auto_20160129_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='sparkterasortinformation',
            name='bench_type',
            field=models.CharField(verbose_name='Bechmark Type', choices=[('Machine Learning-Decison Tree', 'Machine Learning-Decison Tree'), ('Machine Learning-Kmeans', 'Machine Learning-Kmeans'), ('Machine Learning-Lable Propagation', 'Machine Learning-Lable Propagation'), ('Machine Learning-Linear Regression', 'Machine Learning-Linear Regression'), ('Machine Learning-Logistic Regression', 'Machine Learning-Logistic Regression'), ('Machine Learning-Matrix Factorization', 'Machine Learning-Matrix Factorization'), ('Machine Learning-PCA', 'Machine Learning-PCA'), ('Machine Learning-Pregel Operation', 'Machine Learning-Pregel Operation'), ('Machine Learning-Shortest Paths', 'Machine Learning-Shortest Paths'), ('Machine Learning-SVM', 'Machine Learning-SVM'), ('Machine Learning-Connected Component', 'Machine Learning-Connected Component'), ('Machine Learning-Strongly Connected Component', 'Machine Learning-Strongly Connected Component'), ('SQL-RDD Relation', 'SQL-RDD Relation'), ('SQL-HIVE', 'SQL-HIVE'), ('Streaming-Twitter Tag', 'Streaming-Twitter Tag'), ('Streaming-Page View', 'Streaming-Page View'), ('Graph-TriangleCount', 'Graph-TriangleCount'), ('Graph-SVD++', 'Graph-SVD++'), ('Graph-PageRank', 'Graph-PageRank'), ('Search Engine-MicroBenchamrk(Sort,Grep,WordCount)', 'Search Engine-MicroBenchamrk(Sort,Grep,WordCount)'), ('Search Engine-PageRank', 'Search Engine-PageRank'), ('Search Engine-Index', 'Search Engine-Index'), ('Social Networks-Workload MPI_BFS', 'Social Networks-Workload MPI_BFS'), ('Social Networks-Workload MPI_Kmeans', 'Social Networks-Workload MPI_Kmeans'), ('Social Networks-Workload MPI_ConnectedComponent', 'Social Networks-Workload MPI_ConnectedComponent'), ('E-commerce-WorkLoad-Select Query, Aggregation Query, Join Query', 'E-commerce-WorkLoad-Select Query, Aggregation Query, Join Query'), ('E-commerce-Aggregation, Cross Product, Difference, Filter, OrderBy, Project, Union', 'E-commerce-WorkLoad-Select Query, Aggregation Query, Join Query'), ('E-commerce-Recommendation Workload', 'E-commerce-Recommendation Workload'), ('E-commerce-Workload NaiveBayes', 'E-commerce-Workload NaiveBayes'), ('Multimedia analytics-Workload BasicMPEG', 'Multimedia analytics-Workload BasicMPEG'), ('Multimedia analytics-Workload SIFT', 'Multimedia analytics-Workload SIFT'), ('Multimedia analytics-Workload DBN', 'Multimedia analytics-Workload DBN'), ('Multimedia analytics-Workload Speech Recognition', 'Multimedia analytics-Workload Speech Recognition'), ('Multimedia analytics-Workload Ray Tracing', 'Multimedia analytics-Workload Ray Tracing'), ('Multimedia analytics-Workload Image Segmentation', 'Multimedia analytics-Workload Image Segmentation'), ('Multimedia analytics-Workload Face Detection', 'Multimedia analytics-Workload Face Detection'), ('Bioinformatics-Workload SAND', 'Bioinformatics-Workload SAND'), ('Bioinformatics-Workload mpiBLAST', 'Bioinformatics-Workload mpiBLAST')], default='', max_length=128),
        ),
    ]
