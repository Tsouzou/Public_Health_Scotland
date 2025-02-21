import os

def main():
    # Prompt user to input GPPractice numbers separated by space
    gp_input = input("Enter GPPractice numbers separated by space: ")
    gp_practices = gp_input.strip().split()
    
    # Define the PNG filename to check
    png_filename = "OLANZAPINE_TAB.png"
    
    # Directory base path
    base_path = r"C:\MyPythonProjects\Plots"
    
    # List to store GPPractices missing the PNG
    missing_gps = []
    
    # Iterate through each GPPractice number
    for gp in gp_practices:
        # Construct the path to the PNG file
        png_path = os.path.join(base_path, gp, png_filename)
        
        if os.path.exists(png_path):
            print(f"Opening {png_path}")
            os.startfile(png_path)
        else:
            print(f"{gp} is missing {png_filename}")
            missing_gps.append(gp)
    
    # After processing all, list the GPPractices missing the PNG
    if missing_gps:
        print("\nGPPractices with no such PNG:")
        for gp in missing_gps:
            print(gp)
    else:
        print("\nAll specified GPPractices have the PNG file.")

if __name__ == "__main__":
    main()
