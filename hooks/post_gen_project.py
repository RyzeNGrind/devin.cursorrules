import os
import shutil
import platform
from pathlib import Path, PurePath
from tempfile import TemporaryDirectory


def _move_single_file(src_dir: PurePath, dst_dir: PurePath, file_name: str):
    shutil.move(
        str(src_dir.joinpath(file_name)),
        dst_dir.joinpath(file_name),
        copy_function=lambda x, y: shutil.copytree(
            x, y, dirs_exist_ok=True, copy_function=shutil.copy2
        ),
    )


def move_directory_contents(src: PurePath, dst: PurePath):
    temp_dir = TemporaryDirectory()
    temp_dir_path = Path(temp_dir.name)

    directory_contents = os.listdir(src)
    for item in directory_contents:
        print(f"Moving {item} to {temp_dir_path}")
        _move_single_file(src, temp_dir_path, item)

    directory_contents.remove(src.name)

    for item in directory_contents:
        print(f"Moving {item} to {dst}")
        _move_single_file(temp_dir_path, dst, item)

    os.removedirs(src)

    _move_single_file(temp_dir_path, dst, src.name)


def setup_env_file():
    """Set up the .env file with API key if provided"""
    llm_provider = '{{ cookiecutter["llm_provider [Optional. Press Enter to use None]"] }}'
    
    # If provider is local, set up local configuration
    if llm_provider.endswith('(Local)'):
        if not os.path.exists('.env'):
            with open('.env', 'w') as f:
                if llm_provider == 'Ollama (Local)':
                    f.write('OLLAMA_BASE_URL=http://localhost:11434\n')
                elif llm_provider == 'LM Studio (Local)':
                    f.write('LM_STUDIO_BASE_URL=http://localhost:1234\n')
        return

    # If provider != 'None', retrieve whatever was saved in pre_gen_project.py
    if llm_provider != 'None':
        if os.path.exists(".temp_api_key"):
            with open(".temp_api_key", "r") as f:
                llm_api_key = f.read().strip()
            os.remove(".temp_api_key")

            if llm_api_key:
                provider_env_vars = {
                    'OpenAI': 'OPENAI_API_KEY',
                    'Anthropic': 'ANTHROPIC_API_KEY',
                    'DeepSeek': 'DEEPSEEK_API_KEY',
                    'Google': 'GOOGLE_API_KEY',
                    'Azure OpenAI': 'AZURE_OPENAI_API_KEY',
                    'Siliconflow': 'SILICONFLOW_API_KEY'
                }
                env_var_name = provider_env_vars.get(llm_provider)
                if env_var_name:
                    # Update .env or create it if needed
                    if not os.path.exists('.env'):
                        with open('.env', 'w') as _:
                            pass
                    with open('.env', 'r') as f:
                        lines = f.readlines()
                    with open('.env', 'w') as f:
                        key_found = False
                        for line in lines:
                            if line.startswith(env_var_name + '='):
                                f.write(f'{env_var_name}={llm_api_key}\n')
                                key_found = True
                            else:
                                f.write(line)
                        if not key_found:
                            f.write(f'{env_var_name}={llm_api_key}\n')


def handle_ide_rules():
    """Handle IDE-specific rules files based on project type"""
    project_type = '{{ cookiecutter.project_type }}'
    llm_provider = '{{ cookiecutter["llm_provider [Optional. Press Enter to use None]"] }}'
    
    # For Cursor projects: only keep .cursorrules
    if project_type == 'cursor':
        if os.path.exists('.windsurfrules'):
            os.remove('.windsurfrules')
        if os.path.exists('scratchpad.md'):
            os.remove('scratchpad.md')
        if os.path.exists('.github/copilot-instructions.md'):
            os.remove('.github/copilot-instructions.md')
        
        # Update .cursorrules if needed
        if os.path.exists('.cursorrules') and llm_provider == 'None':
            with open('.cursorrules', 'r') as f:
                content = f.readlines()
            
            # Find the Screenshot Verification section and insert the notice before it
            for i, line in enumerate(content):
                if '## Screenshot Verification' in line:
                    content.insert(i, '[NOTE TO CURSOR: Since no API key is configured, please ignore both the Screenshot Verification and LLM sections below.]\n')
                    content.insert(i + 1, '[NOTE TO USER: If you have configured or plan to configure an API key in the future, simply delete these two notice lines to enable these features.]\n\n')
                    break
            
            with open('.cursorrules', 'w') as f:
                f.writelines(content)
    
    # For Windsurf projects: keep both .windsurfrules and scratchpad.md
    elif project_type == 'windsurf':
        if os.path.exists('.cursorrules'):
            os.remove('.cursorrules')
        if os.path.exists('.github/copilot-instructions.md'):
            os.remove('.github/copilot-instructions.md')
        
        # Update .windsurfrules if needed
        if os.path.exists('.windsurfrules') and llm_provider == 'None':
            with open('.windsurfrules', 'r') as f:
                content = f.readlines()
            
            # Find the Screenshot Verification section and insert the notice before it
            for i, line in enumerate(content):
                if '## Screenshot Verification' in line:
                    content.insert(i, '[NOTE TO CURSOR: Since no API key is configured, please ignore both the Screenshot Verification and LLM sections below.]\n')
                    content.insert(i + 1, '[NOTE TO USER: If you have configured or plan to configure an API key in the future, simply delete these two notice lines to enable these features.]\n\n')
                    break
            
            with open('.windsurfrules', 'w') as f:
                f.writelines(content)
    
    # For GitHub Copilot projects: keep .github/copilot-instructions.md
    elif project_type == 'github copilot':
        if os.path.exists('.cursorrules'):
            os.remove('.cursorrules')
        if os.path.exists('.windsurfrules'):
            os.remove('.windsurfrules')
        if os.path.exists('scratchpad.md'):
            os.remove('scratchpad.md')
        
        # Update .github/copilot-instructions.md if needed
        if os.path.exists('.github/copilot-instructions.md') and llm_provider == 'None':
            with open('.github/copilot-instructions.md', 'r') as f:
                content = f.readlines()
            
            # Find the Screenshot Verification section and insert the notice before it
            for i, line in enumerate(content):
                if '## Screenshot Verification' in line:
                    content.insert(i, '[NOTE TO CURSOR: Since no API key is configured, please ignore both the Screenshot Verification and LLM sections below.]\n')
                    content.insert(i + 1, '[NOTE TO USER: If you have configured or plan to configure an API key in the future, simply delete these two notice lines to enable these features.]\n\n')
                    break
            
            with open('.github/copilot-instructions.md', 'w') as f:
                f.writelines(content)


def main():
    """Main function to set up the project"""
    setup_env_file()
    handle_ide_rules()
    
    # Create virtual environment
    print("\nCreating virtual environment...")
    os.system('python3 -m venv venv')
    
    # Install dependencies
    print("\nInstalling dependencies...")
    if platform.system() == 'Windows':
        os.system('venv\\Scripts\\pip install -r requirements.txt')
    else:
        os.system('venv/bin/pip3 install -r requirements.txt')
    
    print("\nSetup completed successfully!")
    print("To get started:")
    print("1. Activate your virtual environment:")
    if platform.system() == 'Windows':
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("2. Check the README.md file for more information")

    if "{{ cookiecutter.use_current_directory }}".lower() == "y":
        import sys
        current_path = Path(os.getcwd()).resolve()
        print(f"\nPOST-GEN DEBUG: Current path: {current_path}")
        
        # Nuclear path resolution
        generated_dir = current_path / "{{ cookiecutter.project_name }}"
        if not generated_dir.exists():
            generated_dir = current_path.parent / "{{ cookiecutter.project_name }}"
            
        print(f"POST-GEN DEBUG: Final generated_dir: {generated_dir}")

        if generated_dir.exists() and generated_dir.is_dir():
            print("MOVING FILES TO PARENT DIRECTORY:")
            # Move all contents including hidden files
            for item in generated_dir.glob('*'):
                dest = current_path / item.name
                print(f"Moving: {item} -> {dest}")
                
                # Nuclear removal of existing files
                if dest.exists():
                    if dest.is_dir():
                        shutil.rmtree(dest, ignore_errors=True)
                    else:
                        try:
                            dest.unlink()
                        except:
                            pass
                
                shutil.move(str(item), str(current_path))
            
            # Remove the now-empty directory
            try:
                generated_dir.rmdir()
                print(f"Removed empty directory: {generated_dir}")
            except OSError as e:
                print(f"Error removing directory: {str(e)}")
            
            print("FILE MOVEMENT COMPLETED SUCCESSFULLY")
        else:
            print(f"ERROR: Generated directory not found at {generated_dir}!")
            sys.exit(1)
