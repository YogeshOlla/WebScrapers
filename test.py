{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "Peeg_miscall_analysis.ipynb",
      "provenance": [],
      "collapsed_sections": []
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "code",
      "execution_count": 97,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "Ger5lR-V1NQF",
        "outputId": "1eb5f6c4-79ac-4851-9368-65004690ebe7"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Drive already mounted at /content/drive; to attempt to forcibly remount, call drive.mount(\"/content/drive\", force_remount=True).\n"
          ]
        }
      ],
      "source": [
        "from google.colab import drive\n",
        "drive.mount('/content/drive')"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import pandas as pd\n",
        "import numpy as np\n",
        "import datetime\n",
        "from datetime import timedelta\n",
        "\n",
        "df=pd.read_csv(\"/content/drive/MyDrive/Hackathons/Text_summarization/Cars v0.2.csv\")\n",
        "df['CREATED_DATE']= pd.to_datetime(df['CREATED_DATE'])"
      ],
      "metadata": {
        "id": "CNgGLMSA1UqG"
      },
      "execution_count": 98,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "incomp=df[(df['CALLER_TYPE']=='Connectcustomer') & (df['CALL_TYPE']=='incomplete')].copy()\n",
        "callbacks = df[(df['CALL_TYPE']=='completed')].copy()\n",
        "rm_failed=df[(df['CALLER_TYPE']=='ConnectRM') & (df['CALL_TYPE']=='incomplete')].copy()\n",
        "callbacks=pd.concat([callbacks, rm_failed])\n",
        "\n",
        "\n",
        "incomp = incomp.sort_values(['CREATED_DATE','APPOINTMENT'],\n",
        "              ascending = [True, True])\n",
        "callbacks = callbacks.sort_values(['CREATED_DATE','APPOINTMENT'],\n",
        "              ascending = [True, True])"
      ],
      "metadata": {
        "id": "_rhYGIK6-g0N"
      },
      "execution_count": 99,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "tol = timedelta(minutes=120)\n",
        "missedcalls = pd.merge_asof(incomp,callbacks[['CREATED_DATE','APPOINTMENT']],on='CREATED_DATE',by='APPOINTMENT',direction='forward',tolerance=tol)\n",
        "out=missedcalls.groupby('CONNECTED_WITH')['APPOINTMENT'].count()"
      ],
      "metadata": {
        "id": "2YU6k-fkKaCc"
      },
      "execution_count": 101,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "out.to_csv('/content/drive/MyDrive/Hackathons/Text_summarization/pig_out_qc.csv')"
      ],
      "metadata": {
        "id": "0eIS2lB7LXGD"
      },
      "execution_count": 102,
      "outputs": []
    }
  ]
}