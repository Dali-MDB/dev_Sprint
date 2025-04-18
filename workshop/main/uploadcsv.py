import csv
import io
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status

class CSVUploadAPIView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'error': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check extension
        if not file_obj.name.endswith('.csv'):
            return Response({'error': 'Only CSV files are supported.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            decoded_file = file_obj.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.reader(io_string)
            
            header = next(reader)  # First row = header
            rows = []
            for row in reader:
                rows.append(dict(zip(header, row)))  # Map header to values

            return Response({
                'message': 'CSV processed successfully.',
                'columns': header,
                'rows': rows[:5]  # Preview first 5 rows
            })

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)




#import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status

class CSVUploadAPIView(APIView):
    parser_classes = [MultiPartParser]  # Handles file uploads

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file', None)
        if not file_obj:
            return Response({'error': 'No file uploaded.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check file type
        if not file_obj.name.endswith('.csv'):
            return Response({'error': 'Uploaded file is not a CSV.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
           # df = pd.read_csv(file_obj)

            # Optional: show a preview of the first few rows
            #data_preview = df.head().to_dict(orient='records')
            data_preview = "test"

            # Optional: save to model here

            return Response({
                'message': 'CSV uploaded successfully.',
                'preview': data_preview,
                #'columns': df.columns.tolist(),
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

