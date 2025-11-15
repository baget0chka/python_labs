import re
    
def translate_cpp_to_python(input, output):
    lines = input.split('\n')
    out_file = open(output, "w")

    indent_level = 0
    in_case = False
    in_switch = False
    is_main = False
    in_class = False
    class_fields = {}
    current_access = "public"
    current_class = ""
    constructor_was = False

    for line in lines:
        vector_init_match = re.search(r"std::vector<int>\s+(\w+)\s*=\s*\{([^}]+)\}", line)
        if vector_init_match:
            var_name = vector_init_match.group(1)
            elements = vector_init_match.group(2)
            out_file.write("\t" * indent_level + f"{var_name} = [{elements}]\n")
            continue

        close_braces_matches = re.search(r'\}', line)
        if close_braces_matches:
            if indent_level > 0:
                indent_level -= 1
            if in_switch and not in_case:
                in_switch = False
            elif in_class and indent_level == 0:
                in_class = False
                class_name = ""
            continue

        include_match = re.search("#include", line)
        tamplate_match = re.search("template<typename T>", line)
        function_match = re.search(r"(void|int|long|T|float|std::string|bool|std::vector<T>|std::vector<int>) (\w+)\s*\((.*)\)\s*{?", line)
        cin_match = re.search(r"std::cin\s*>>\s*(\w+)", line)
        cout_match = re.search(r'<<\s*([^;]+)', line)
        if_match = re.search(r"if\s*\((.+)\)", line)
        for_match = re.search(r"for\s*\(\s*int\s*(\w+)\s*=\s*([^;]+);\s*(\w+)\s*(<|>|>=|<=){1}\s*([^;]+);\s*(\w+)(\+\+|\-\-)", line)
        switch_match = re.search(r"switch\s*\((\w+)\)", line)
        case_match = re.search(r"case\s*(\d+):", line)
        while_match = re.search(r"while\s*\((.+)\)", line)
        init_var_match = re.search(r"(int|float|std::string|T|bool|std::vector<T>|std::vector<int>)\s+([^;]+);", line)
        class_match = re.search(r"class\s+(\w+)\s*(:\s*public\s+(\w+))?\s*{", line)
        access_match = re.search(r"(public|protected|private):", line)
        constructor_match = re.search(r"(\w+)\s*\((.*?)\)\s*{?", line)
        assignment_match = re.search(r"(\w+)\s*=\s*([^;]+);", line)
        return_match = re.search(r"return\s+(.+);", line)
        class_instance_match = re.match(r"\s*(\w+)\s+(\w+)\s*\((.*)\);", line)

        if include_match or tamplate_match:
            continue

        if class_match:
            class_name = class_match.group(1)
            base_class = class_match.group(3)
            current_access = "public"
            current_class = class_name
            constructor_was = False

            if base_class:
                out_file.write("\t" * indent_level + f"class {class_name}({base_class}):" + "\n")
            else:
                out_file.write("\t" * indent_level + f"class {class_name}:" + "\n")

            in_class = True
            indent_level += 1
            continue

        if access_match:
            current_access = access_match.group(1)
            continue

        if constructor_match and in_class and constructor_match.group(1) == current_class:
            constructor_was = True
            args_to_parse = constructor_match.group(2)

            args = re.sub(r"\b(const\s+)?(std::string|int|float|double|bool|Animal|T)\s*(&\s*)?", "", args_to_parse)
            args = args.replace("false", "False").replace("true", "True")

            init_list_match = re.search(r":\s*(\w+\([^)]+\))", line)
            if init_list_match:
                init_call = init_list_match.group(1)
                out_file.write("\t" * indent_level + f"super().__init__({init_call.split('(')[1][:-1]})" + "\n")

            out_file.write("\t" * indent_level + f"def __init__(self, {args}):" + "\n")
            indent_level += 1
            continue
    
        if function_match:
            function_name = function_match.group(2)
            args = function_match.group(3)
            args = re.sub(r"\b(const\s+)?(std::string|int|float|double|bool|Animal|std::vector<T>|T|std::vector<int>)\s*(&\s*)?", "", args)
            if in_class:
                if args:
                    args = "self, " + args
                else:
                    args = "self"
            if function_name == "main":
                out_file.write("\t" * indent_level + f"if __name__ == '__main__':" + "\n")
                is_main = True
            else:
                out_file.write("\t" * indent_level + f"def {function_name}({args}):" + "\n")
            indent_level += 1
            continue

        if cin_match:
            cin = cin_match.group(1)
            out_file.write("\t" * indent_level + f"{cin} = float(input())" + "\n")
            continue

        if cout_match:
            to_print = ""
            parts = cout_match.group(1).split("<<")
            need_new = False

            for p in parts:
                if "std::endl" in p:
                    need_new = True
                    continue
                if in_class:
                    if p.strip() in class_fields:
                        p = "self." + class_fields.get(p.strip(), p)
                to_print += p
                if (len(parts) != 1) or ((len(parts) == 2) and ("std::endl" in parts)):
                    to_print += ","

            if (len(to_print) > 0) and (to_print[-1] == ","):
                to_print = to_print[:-1]

            if need_new:
                out_file.write("\t" * indent_level + f"print({to_print})" + "\n")
            else:
                out_file.write("\t" * indent_level + f"print({to_print}, end='')" + "\n")
            
            continue

        if if_match:
            condition = if_match.group(1)
            condition = condition.replace("&&", "and").replace("||", "or").replace("!=", "#").replace("!", "not ").replace("#", "!=")
            if in_class:
                parts = condition.split(" ")
                condition = ""
                for p in parts:
                    if p.strip() in class_fields:
                        p = "self." + class_fields.get(p)
                    if p in ["and", "or", "!=", "not"]:
                        p = " " + p + " "
                    condition += p
            out_file.write("\t" * indent_level + f"if {condition}:" + "\n")
            indent_level += 1
            continue

        if re.search(r"else\s*{", line):
            out_file.write("\t" * indent_level + f"else:" + "\n")
            indent_level += 1
            continue

        if for_match:
            var = for_match.group(1)
            start = for_match.group(2)
            sign = for_match.group(4)
            end = for_match.group(5)
            direction = for_match.group(7)
            if sign in [">=", "<="]:
                end = end + 1
            if direction == "++":
                direction = 1
            else: 
                direction = -1

            out_file.write("\t" * indent_level + f"for {var} in range({start}, {end}, {direction}):" + "\n")
            indent_level += 1
            continue

        if switch_match:
            var = switch_match.group(1)
            out_file.write("\t" * indent_level + f"match {var}:" + "\n")
            indent_level += 1
            in_switch = True
            continue

        if case_match:
            val = case_match.group(1)
            out_file.write("\t" * indent_level + f"case {val}:" + "\n")
            indent_level += 1
            in_case = True
            continue

        if re.search(r"break\s*;", line) and in_case:
            if indent_level > 0:
                indent_level -= 1
            in_case = False
            continue

        if re.search(r"default", line) and in_switch:
            in_case = True
            out_file.write("\t" * indent_level + f"case _:" + "\n")
            indent_level += 1
            continue

        if while_match:
            condition = while_match.group(1)
            condition = condition.replace("&&", "and").replace("||", "or").replace("!=", "#").replace("!", "not").replace("#", "!=")

            out_file.write("\t" * indent_level + f"while {condition}:" + "\n")
            indent_level += 1
            continue

        if return_match:
            if is_main:
                continue
            if in_class:
                return_value = return_match.group(1)
                if return_value in class_fields:
                    return_value = "self." + class_fields.get(return_value)
                    out_file.write("\t" * indent_level + f"return {return_value}" + "\n")
                    continue
        
        if init_var_match:
            type = init_var_match.group(1)
            to_parse = init_var_match.group(2)
            
            vars = [v.strip() for v in to_parse.split(',')]

            if type in {"int", "float"}:
                type_val = 0

            elif type == "std::string":
                type_val = "''"

            elif type == "bool":
                type_val = False

            elif type == "std::vector<T>" or type == "std::vector<int>":
                type_val = []

            else: 
                type_val = None

            for var in vars:
                if '=' in var:
                    var_name, var_value = var.split('=')
                    var_name = var_name.strip()
                    var_value = var_value.strip()
                    var_value = var_value.replace("false", "False").replace("true", "True")
                    
                    size_match = re.search(r"\s*(\w+)\.size\(\)", var_value)
                    if size_match:
                        var_len = size_match.group(1)

                        var_value = var_value.replace(f"{var_len}.size()", f"len({var_len})")

                    ternary_match = re.match(r'\((.+)\?(.+):(.+)\)', var_value)
                    if ternary_match:
                        condition = ternary_match.group(1).strip()
                        if condition in class_fields:
                            condition = "self." + class_fields[condition]
                        true_val = ternary_match.group(2).strip()
                        false_val = ternary_match.group(3).strip()
                        var_value = f"{{{true_val} if {condition} else {false_val}}}"

                    key = var_name
                    if in_class:
                        if current_access == "protected" or current_access == "private":
                            if current_access == "private":
                                var_name = "__" + var_name
                            else:
                                var_name = "_" + var_name
                            class_fields[key] = var_name
                        if constructor_was and var.strip() in class_fields:
                            out_file.write("\t" * indent_level + f"self.{class_fields.get(key, var_name)} = {var_value}" + "\n")
                        else:
                            out_file.write("\t" * indent_level + f"{class_fields.get(key, var_name)} = {var_value}" + "\n")
                        continue
                    out_file.write("\t" * indent_level + f"{var_name} = {var_value}" + "\n")
                else:
                    if in_class:
                        key = var
                        if current_access == "protected" or current_access == "private":
                            if current_access == "private":
                                var = "__" + var
                            else:
                                var = "_" + var
                            class_fields[key] = var
                        if constructor_was and var.strip() in class_fields:
                            out_file.write("\t" * indent_level + f"self.{var} = {type_val}" + "\n")
                        else:
                            out_file.write("\t" * indent_level + f"{var} = {type_val}" + "\n")
                        continue
                    out_file.write("\t" * indent_level + f"{var} = {type_val}" + "\n")
            continue

        if assignment_match:
            var_name = assignment_match.group(1)
            value = assignment_match.group(2)
            value = value.replace("true", "True").replace("false", "False").replace("std::pow", "pow")
            
            if in_class:
                var_name = class_fields.get(var_name, var_name)
                out_file.write("\t" * indent_level + f"self.{var_name} = {value}" + "\n")
            else: 
                out_file.write("\t" * indent_level + f"{var_name} = {value}" + "\n")
            continue
        
        if class_instance_match:
            class_name = class_instance_match.group(1)
            var_name = class_instance_match.group(2)
            args = class_instance_match.group(3).strip()

            args = args.replace("false", "False").replace("true", "True")

            out_file.write("\t" * indent_level + f"{var_name} = {class_name}({args})\n")
            continue

        line = line.strip().replace(";", "")
        out_file.write("\t" * indent_level + line + "\n")


if __name__ == "__main__": 

    for i in range(3):
        file = open(f"./testFiles/{i+1}.cpp", "r")
        cpp_code = file.read()
        file.close()

        out_file_name = f"./outputFiles/{i+1}.py"

        translate_cpp_to_python(cpp_code, out_file_name)