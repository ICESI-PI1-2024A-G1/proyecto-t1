import json
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


class SharePointAPI:
    def __init__(self, excel_path: str) -> None:
        self.excel_path = excel_path

    @csrf_exempt
    def get_all_requests(self, request):
        # Ruta para obtener todas las solicitudes
        if request.method == "GET":
            # Lee el archivo Excel
            try:
                df = pd.read_excel(self.excel_path, sheet_name="requests")
            except FileNotFoundError:
                return JsonResponse({"error": "El archivo no se encontró"}, status=404)

            # Convierte los datos a formato JSON
            data = df.to_dict(orient="records")

            return JsonResponse(data, safe=False)

    @csrf_exempt
    def update_data(self, request):
        # Ruta para consultar datos
        if request.method == "GET":
            # Lee el archivo Excel
            try:
                df = pd.read_excel(self.excel_path, sheet_name="data")
            except FileNotFoundError:
                return JsonResponse({"error": "El archivo no se encontró"}, status=404)

            # Convierte los datos a formato JSON
            data = df.to_dict(orient="records")

            return JsonResponse(data, safe=False)

    @csrf_exempt
    def create_data(self, data):
        # Ruta para crear un nuevo dato
        try:
            df = pd.read_excel(self.excel_path, sheet_name="data")
            df = df.append(data, ignore_index=True)
            df.to_excel(self.excel_path, sheet_name="data", index=False)
        except FileNotFoundError:
            return {"error": "El archivo no se encontró"}, 404
        return {"mensaje": "Dato creado satisfactoriamente"}, 201

    @csrf_exempt
    def update_data(self, request, id):
        # Ruta para actualizar un dato existente
        if request.method == "PUT":
            # Obtener los datos del cuerpo de la solicitud
            body_unicode = request.body.decode("utf-8")
            body = json.loads(body_unicode)

            # Actualizar el dato con el ID proporcionado
            try:
                df = pd.read_excel(self.excel_path, sheet_name="data")
                df.loc[df["id"] == id] = body
                df.to_excel(self.excel_path, sheet_name="data", index=False)
            except FileNotFoundError:
                return JsonResponse({"error": "El archivo no se encontró"}, status=404)

            return JsonResponse({"mensaje": "Dato actualizado satisfactoriamente"})

    @csrf_exempt
    def delete_data(self, request, id):
        # Ruta para eliminar un dato existente
        if request.method == "DELETE":
            # Eliminar el dato con el ID proporcionado
            try:
                df = pd.read_excel(self.excel_path, sheet_name="data")
                df = df[df["id"] != id]
                df.to_excel(self.excel_path, sheet_name="data", index=False)
            except FileNotFoundError:
                return JsonResponse({"error": "El archivo no se encontró"}, status=404)

            return JsonResponse({"mensaje": "Dato eliminado satisfactoriamente"})
