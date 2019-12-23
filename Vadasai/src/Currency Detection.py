#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3
import cv2

client = boto3.client('s3', region_name='us-west-2')

def detect_labels(photo, bucket):

    client=boto3.client('rekognition')

    response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},
        MaxLabels=10)

    for label in response['Labels']:
        if(label['Name']=="Money" and label['Confidence']>65):
            return "YES"

    print("no chance of any money")


def detect_text(photo, bucket):

    client=boto3.client('rekognition')

    response=client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':photo}})
                        
    textDetections=response['TextDetections']
    for text in textDetections:
            
            if(text['DetectedText']=="FIVE" or text['DetectedText']=='5'):
                return 5
            elif(text['DetectedText']=="TEN"or text['DetectedText']=='10'):
                return 10
            elif(text['DetectedText']=="FIFTY"or text['DetectedText']=='50'):
                return 50
            elif(text['DetectedText']=="TWO"or text['DetectedText']=='200'):
                return 200
            elif(text['DetectedText']=="HUNDRED"or text['DetectedText']=='100'):
                return 100
            elif(text['DetectedText']=="TWENTY" or text['DetectedText']=='20'):
                return 20
    return 20




def main():
    d=0
    cap = cv2.VideoCapture('Input/checkmoney.mp4')
    while(d<4):
        status,img=cap.read()
        if cv2.waitKey(5) & 0xFF == ord('c'):
            cv2.imwrite('Output/Currency/20.jpeg',img)
            client.upload_file('Output/Currency/20.jpeg', 'awssamyak', 'image_0.jpg')
            is_money=detect_labels("image_0.jpg", "awssamyak")

            if(is_money=="YES"):
                note_value=detect_text("image_0.jpg", "awssamyak")
                print(note_value)
            d+=1
        cv2.imshow('img',img)

    cap.release()
    cv2.destroyAllWindows()


    
    


if __name__ == "__main__":
    main()



