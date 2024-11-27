import pandas as pd
def extract_link_bases(file_path):
    link_bases = []
    links = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()  # Remove leading/trailing whitespace and newline characters
                links.append(line)
                if line:
                    parts = line.split("/")
                    if len(parts) >= 3:  # Check if the link has at least three parts
                        base = parts[-1]
                        link_bases.append(base)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    return link_bases , links

def main():
    print("creating dataframe")
    file_path = 'channels_links.txt'  # Replace with the path to your file
    link_bases , links = extract_link_bases(file_path)

    data = {"name":link_bases,"link":links}
    link_frame = pd.DataFrame(data=data)
    link_frame.to_csv('channel_table.txt',sep='\t') 


if __name__ == '__main__':
    main()




