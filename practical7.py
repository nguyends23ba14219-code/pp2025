import subprocess
import os

def execute_command(command_line):
    """
    Parses and executes a command line string with support for:
    - Standard execution
    - Output redirection (>)
    - Input redirection (<)
    - Pipes (|)
    """
    try:
        if '|' in command_line:
            processes = command_line.split('|')
            prev_proc = None
            
            for i, cmd_str in enumerate(processes):
                cmd_str = cmd_str.strip()
                cmd_parts = cmd_str.split()
    
                stdin = prev_proc.stdout if prev_proc else None
    
                stdout = subprocess.PIPE if i < len(processes) - 1 else None

                curr_proc = subprocess.Popen(
                    cmd_parts, 
                    stdin=stdin, 
                    stdout=stdout, 
                    text=True
                )
          
                if prev_proc:
                    prev_proc.stdout.close()
                
                prev_proc = curr_proc
      
            if prev_proc:
                prev_proc.communicate()
            return

        if '>' in command_line:
            parts = command_line.split('>')
            cmd_part = parts[0].strip().split()
            file_part = parts[1].strip()
            
            with open(file_part, 'w') as f:
                subprocess.run(cmd_part, stdout=f, check=True)
            return

        if '<' in command_line:
            parts = command_line.split('<')
            cmd_part = parts[0].strip().split()
            file_part = parts[1].strip()
            
            with open(file_part, 'r') as f:
                subprocess.run(cmd_part, stdin=f, check=True)
            return

        subprocess.run(command_line.split(), check=True)

    except FileNotFoundError:
        print(f"Command not found: {command_line}")
    except Exception as e:
        print(f"Error executing command: {e}")

def main():
    print("Welcome to Python Shell. Type 'exit' to quit.")
    while True:
        try:
            command = input(f"{os.getcwd()}$ ")
            
            if command.strip() == 'exit':
                break
            if not command.strip():
                continue
                
            execute_command(command)
            
        except KeyboardInterrupt:
            print("\nType 'exit' to quit.")

if __name__ == "__main__":
    main()