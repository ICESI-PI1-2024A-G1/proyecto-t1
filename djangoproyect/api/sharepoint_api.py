import json
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


class SharePointAPI:
    def __init__(self, excel_path) -> None:
        self.excel_path = excel_path
        self.columns_names = [
            "document",
            "applicant",
            "manager",
            "initial_date",
            "final_date",
            "past_days",
            "status",
            "type",
            "description",
            "title",
            "assigned_users",
        ]

    @csrf_exempt
    def obtain_single_data(self, id):
        try:
            # Lee el archivo Excel
            df = pd.read_excel(self.excel_path, sheet_name="data")
        except FileNotFoundError:
            return JsonResponse({"error": "El archivo no se encontró"}, status=404)

        # Encuentra el dato con el ID proporcionado
        data = df[df["id"] == id].to_dict(orient="records")

        if not data:
            return JsonResponse(
                {"error": "No se encontró el dato con el ID proporcionado"},
                status=404,
            )

        return JsonResponse(data[0], safe=False)

    @csrf_exempt
    def get_all_requests(self):
        try:
            df = pd.read_excel(self.excel_path, sheet_name="data")
        except FileNotFoundError:
            return JsonResponse({"error": "El archivo no se encontró"}, status=404)

        # Convierte los datos a formato JSON
        data = df.to_dict(orient="records")

        return JsonResponse(data, safe=False)

    @csrf_exempt
    def update_data(self):
        try:
            df = pd.read_excel(self.excel_path, sheet_name="data")
        except FileNotFoundError:
            return JsonResponse({"error": "El archivo no se encontró"}, status=404)

        # Convierte los datos a formato JSON
        data = df.to_dict(orient="records")

        return JsonResponse(data, safe=False)

    @csrf_exempt
    def create_data(self, data):
        try:
            excel_file = pd.ExcelFile(self.excel_path)

            if "data" in excel_file.sheet_names:
                df = pd.read_excel(
                    self.excel_path, sheet_name="data", names=self.columns_names
                )
            else:
                df = pd.DataFrame(columns=self.columns_names)

            df = df.append(data, ignore_index=True)

            with pd.ExcelWriter(
                self.excel_path, mode="a", if_sheet_exists="overlay"
            ) as writer:
                df.to_excel(
                    writer,
                    sheet_name="data",
                    index=False,
                    header=False,
                    startrow=writer.sheets["data"].max_row,
                )

            return 201
        except Exception as e:
            print(f"Error: {e}")
            return 500

    @csrf_exempt
    def update_data(self, new_data, id):
        body = json.loads(new_data)

        # Actualizar el dato con el ID proporcionado
        try:
            df = pd.read_excel(self.excel_path, sheet_name="data")
            df.loc[df["id"] == id] = body
            df.to_excel(self.excel_path, sheet_name="data", index=False)
        except FileNotFoundError:
            return JsonResponse({"error": "El archivo no se encontró"}, status=404)

        return JsonResponse({"mensaje": "Dato actualizado satisfactoriamente"})

    @csrf_exempt
    def delete_data(self, id):
        try:
            df = pd.read_excel(self.excel_path, sheet_name="data")
            df = df[df["id"] != id]
            df.to_excel(self.excel_path, sheet_name="data", index=False)
        except FileNotFoundError:
            return JsonResponse({"error": "El archivo no se encontró"}, status=404)

        return JsonResponse({"mensaje": "Dato eliminado satisfactoriamente"})
