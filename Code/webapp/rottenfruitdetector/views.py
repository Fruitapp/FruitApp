from django.shortcuts import render
from rottenfruitdetector.classifier import classify, newClassify, load_image, rotten_classifier
import requests
from io import BytesIO
import boto3
import tempfile
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rottenfruitdetector.serializers.sampleSerializer import SampleSerializer


def index(request):
    """View function for home page of site."""
    # Render the HTML template index.html with the data in the context variable
    category = None
    is_rotten = 0
    if request.method == 'POST':
        if request.POST['url']:
            fd = BytesIO(requests.get(request.POST['url']).content)
        elif 'file' in request.FILES:
            fd = request.FILES['file']

        
        x = load_image(fd)

        prediction = classify(x, 'fruits')
        
        try:
            category = [x for x, y in zip(['apples', 'bananas', 'oranges'], prediction) if y > 0.99][0]
        except IndexError:
            category = 'unknown'

        if category != 'unknown':
            is_rotten = classify(x, category)

        print(category, is_rotten)
    return render(request, 'index.html', context={'category': category, 'is_rotten': is_rotten})

@api_view(['GET', 'POST'])
def classifier(request):
    if request.method == 'GET':
        my_response = {
            "imageId" : "hola.jpg",
            "rotten"  : 0 
        }
        my_serializer = SampleSerializer(data=my_response)
        my_serializer.is_valid(True)
        return Response(my_serializer.data)
    
    if request.method == 'POST':
        # Process Request
        imgName = request.data["imgId"]
        secretKey = request.data["secret"]
        fruitType = request.data["fruitType"]
        if secretKey != "secretKey":
            return Response("Error de autenticación")
        
        s3 = boto3.resource('s3', region_name='us-west-1',aws_access_key_id='AKIA35RUPLHOZXWR4NXW',aws_secret_access_key= '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')

        bucket = s3.Bucket('myfruitappbucket')
        s3_file = bucket.Object('fruit-detection/' + imgName)
        tmp = tempfile.NamedTemporaryFile()
        rotten = True
        #convertira aun BytesIO
        # category = rottenClassifier(x, fruitType)
        with open(tmp.name, 'wb') as f:
            s3_file.download_fileobj(f)
            fd = BytesIO(s3_file.get()['Body'].read())
            x = load_image(fd)
            print(tmp.name)
            rotten = bool(classify(x, fruitType))
            print(rotten)


        response = Response({"rotten" : rotten})
        response["Access-Control-Allow-Origin"] = "*"
        print(response._headers)
        return response

@api_view(['POST'])
def multiClassifier(request):
    if request.method == 'POST':
        # Process Request
        imgName = request.data["imgId"]
        secretKey = request.data["secret"]
        fruitType = request.data["fruitType"]
        if secretKey != "secretKey":
            return Response("Error de autenticación")
        
        s3 = boto3.resource('s3', region_name='us-west-1',aws_access_key_id='AKIA35RUPLHOZXWR4NXW',aws_secret_access_key= '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')

        bucket = s3.Bucket('myfruitappbucket')
        s3_file = bucket.Object('fruit-detection/' + imgName)
        tmp = tempfile.NamedTemporaryFile()
        state = True
        #convertira aun BytesIO
        # category = rottenClassifier(x, fruitType)
        with open(tmp.name, 'wb') as f:
            s3_file.download_fileobj(f)
            fd = BytesIO(s3_file.get()['Body'].read())
            x = load_image(fd)
            print(tmp.name)

            state = newClassify(x, fruitType)
            print(state)
        if(state[0] == 1.0) :
            response = Response({"state" : "inmaduro" })
        elif(state[1] == 1.0) :
            response = Response({"state" : "maduro" })
        elif(state[2] == 1.0) :
            response = Response({"state" : "podrido" })

        response["Access-Control-Allow-Origin"] = "*"
        print(response._headers)
        return response  