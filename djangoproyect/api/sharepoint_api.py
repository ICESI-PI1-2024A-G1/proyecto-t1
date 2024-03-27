import json
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


class SharePointAPI:
    def __init__(self, excel_path) -> None:
        self.excel_path = excel_path

    @csrf_exempt
    def get_request_by_id(self, id):
        try:
            df = pd.read_excel(self.excel_path, sheet_name="data", header=0)
        except FileNotFoundError:
            return JsonResponse({"error": "El archivo no se encontró"}, status=404)

        data = df[df["id"] == id].to_dict(orient="records")
        return data[0]

    @csrf_exempt
    def get_all_requests(self):
        try:
            df = pd.read_excel(self.excel_path, sheet_name="data", header=0)
        except FileNotFoundError:
            return JsonResponse({"error": "El archivo no se encontró"}, status=404)
        data = df.to_dict(orient="records")
        return data

    @csrf_exempt
    def update_data(self):
        try:
            df = pd.read_excel(self.excel_path, sheet_name="data", header=0)
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
                df = pd.read_excel(self.excel_path, sheet_name="data")
                start_row = len(df)
            else:
                df = pd.DataFrame()
                start_row = 0

            new_data = data.copy()
            new_data["assigned_users"] = ",".join(
                [str(user) for user in new_data["assigned_users"]]
            )

            new_data["id"] = start_row + 1

            new_df = pd.DataFrame([new_data])

            result = pd.concat([df, new_df], ignore_index=True)

            # print("DataFrame antes de guardar en el archivo Excel:")
            # print(result)

            # Escribir el DataFrame actualizado en el archivo Excel
            result.to_excel(
                self.excel_path,
                sheet_name="data",
                index=False,
                columns=[
                    "id",  # Agregar el ID como la primera columna
                    "document",
                    "applicant",
                    "manager",
                    "initial_date",
                    "final_date",
                    "past_days",
                    "description",
                    "title",
                    "status",
                    "req_type",
                    "assigned_users",
                ],
            )

            return 201
        except Exception as e:
            print(f"Error: {e}")
            return 500

    @csrf_exempt
    def update_data(self, id, new_data):

        # Actualizar el dato con el ID proporcionado
        try:
            df = pd.read_excel(self.excel_path, sheet_name="data", header=0)
            # Buscar la fila con el ID proporcionado y actualizar sus valores
            mask = df["id"] == id
            if not df[mask].empty:
                for column_name, new_value in new_data.items():
                    df.loc[mask, column_name] = new_value

                df.to_excel(self.excel_path, sheet_name="data", index=False)
                return JsonResponse({"mensaje": "Dato actualizado satisfactoriamente"})
        except FileNotFoundError:
            return JsonResponse({"error": "El archivo no se encontró"}, status=404)

        return JsonResponse({"mensaje": "Dato actualizado satisfactoriamente"})

    @csrf_exempt
    def delete_data(self, id):
        try:
            df = pd.read_excel(self.excel_path, sheet_name="data", header=0)
            df = df[df["id"] != id]
            df.to_excel(self.excel_path, sheet_name="data", index=False)
        except FileNotFoundError:
            return JsonResponse({"error": "El archivo no se encontró"}, status=404)

        return JsonResponse({"mensaje": "Dato eliminado satisfactoriamente"})
