import win32com.client
import os


def convert_dxf_to_dwg(dxf_file, directory):
    # Create an AutoCAD COM object
    autocad = win32com.client.Dispatch("AutoCAD.Application")
    # autocad.Visible = True
    # Construct the full path to the DXF file
    dxf_path = os.path.join(directory, dxf_file)
    # Open the DXF file
    doc = autocad.Documents.Open(dxf_path)
    # Generate the DWG file path in the same directory
    dwg_file = os.path.join(directory, os.path.splitext(dxf_file)[0] + '.dwg')
    # Save the file as DWG
    doc.SaveAs(dwg_file, 24)  # 24 represents the DWG format for AutoCAD 2010
    # Close the document
    doc.Close()

    # Quit AutoCAD application
    # autocad.Quit()


if __name__ == "__main__":
    directory = r"D:\20240113 SIDC项目\Python\res"
    d2 = r"D:\20240113 SIDC项目\Python\20240709 互通区总体"
    convert_dxf_to_dwg("互通区基础平面-240806.dxf", directory)
    # convert_dxf_to_dwg("互通区墩柱平面-240802.dxf", directory)
    # convert_dxf_to_dwg("互通区盖梁平面-240802.dxf", directory)
    # convert_dxf_to_dwg("互通区盖梁顶推荐标高-240801.dxf", d2)
