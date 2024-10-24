import heapq, os

class BinaryTree:
    def __init__(self, value, frequ):
        self.value = value
        self.frequ = frequ
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequ < other.frequ

    def __eq__(self, other):
        return self.frequ == other.frequ


class Huffmancode:

    def __init__(self, path):
        self.path = path
        self.__heap = []
        self.__code = {}
        self.__reversecode = {}

    def __frequency_from_text(self, text):
        frequ_dict = {}
        for char in text:
            if char not in frequ_dict:
                frequ_dict[char] = 0
            frequ_dict[char] += 1
        return frequ_dict

    def __build_heap(self, frequency_dict):
        for key in frequency_dict:
            frequency = frequency_dict[key]
            binary_tree_node = BinaryTree(key, frequency)
            heapq.heappush(self.__heap, binary_tree_node)

    def __build_binary_tree(self):
        while len(self.__heap) > 1:
            binary_tree_node_1 = heapq.heappop(self.__heap)
            binary_tree_node_2 = heapq.heappop(self.__heap)
            sum_of_freq = binary_tree_node_1.frequ + binary_tree_node_2.frequ
            newnode = BinaryTree(None, sum_of_freq)
            newnode.left = binary_tree_node_1
            newnode.right = binary_tree_node_2
            heapq.heappush(self.__heap, newnode)
        return

    def __build_tree_code_helper(self, root, curr_bits):
        if root is None:
            return
        if root.value is not None:
            self.__code[root.value] = curr_bits
            self.__reversecode[curr_bits] = root.value
            return
        self.__build_tree_code_helper(root.left, curr_bits + '0')
        self.__build_tree_code_helper(root.right, curr_bits + '1')

    def __build_tree_code(self):
        root = heapq.heappop(self.__heap)
        self.__build_tree_code_helper(root, '')

    def __build_encoded_text(self, text):
        encoded_text = ''
        for char in text:
            encoded_text += self.__code[char]
        return encoded_text

    def __build_padded_text(self, encoded_text):
        padding_value = 8 - len(encoded_text) % 8
        for i in range(padding_value):
            encoded_text += '0'

        padded_info = "{0:08b}".format(padding_value)
        padded_text = padded_info + encoded_text
        return padded_text

    def __build_bite_array(self, padded_text):
        array = []
        for i in range(0, len(padded_text), 8):
            byte = padded_text[i:i + 8]
            array.append(int(byte, 2))
        return array

    def compression(self):
        print("Compression for your file starts...")

        # To access the file and extract text from that file.
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + '.bin'
        with open(self.path, 'r+') as file, open(output_path, 'wb') as output:
            text = file.read()
            text = text.rstrip()
            frequency_dict = self.__frequency_from_text(text)

            # Calculate frequency of each text and store it in the frequency dictionary.
            self.__build_heap(frequency_dict)

            # Construct binary tree from the heap.
            self.__build_binary_tree()

            # Construct code from binary tree and store it in a dictionary.
            self.__build_tree_code()

            # Construct the encoded text.
            encoded_text = self.__build_encoded_text(text)

            # Padding of encoded text.
            padded_text = self.__build_padded_text(encoded_text)

            # Return that binary file as an output.
            bytes_array = self.__build_bite_array(padded_text)
            final_bytes = bytes(bytes_array)
            output.write(final_bytes)

        print('Compressed successfully')
        return output_path

    def __remove_padding(self, bit_string):
        # First 8 bits contain the padded information (padding value)
        padded_info = bit_string[:8]
        padding_value = int(padded_info, 2)  # Convert the 8-bit binary number to an integer

        # Remove the first 8 bits and the actual padding from the end
        bit_string = bit_string[8:]
        text = bit_string[:-padding_value]  # Remove padding bits from the end of the bit string

        return text

    def __decoded_text(self, text):
        current_bits = ''
        decoded_text = ''
        for char in text:
            current_bits += char
            if current_bits in self.__reversecode:
                decoded_text += self.__reversecode[current_bits]
                current_bits = ''
        return decoded_text

    def decompress(self, input_path):
        filename, file_extension = os.path.splitext(input_path)
        output_path = filename + '_decompressed' + '.txt'
        with open(input_path, 'rb') as file, open(output_path, 'w') as output:
            bit_string = ''
            byte = file.read(1)
            while byte:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)

            # Remove padding from the bit string
            text_after_removing_padding = self.__remove_padding(bit_string)

            # Decode the text
            actual_text = self.__decoded_text(text_after_removing_padding)
            output.write(actual_text)

        print(f"Decompressed successfully into {output_path}")
        return output_path


# Example usage
path = input("Enter the path of the file which you want to compress: ")
h = Huffmancode(path)
compressed_file = h.compression()
h.decompress(compressed_file)
