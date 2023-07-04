import docker
import os


def main():
    docker_client = docker.from_env()

    # print('Is server responsive:')
    # print(docker_client.ping())

    # print('\nPulling nginx image')
    # print(docker_client.images.pull('nginx'), '\n')

    # images = docker_client.images.list(all=True)
    # print('\nImage list:')
    # for image in images:
    #     print('ID: ', image.id)
    #     print(f'Tags: {image.tags}\n')

    # print('Container creation: client.containers.run("ubuntu:latest", "echo hello world")')
    # print(docker_client.containers.run("ubuntu:latest", "echo hello world"), "\n")

    # containers = docker_client.containers.list(all=True)
    # print('Container list:')
    # for container in containers:
    #     print('ID: ', container.id)
    #     print('Name: ', container.name)
    #     print('Image: ', container.image)
    #     print(f'Status: ${container.status}\n')

    # optional_container = next((c for c in containers if 'whalesay-py' in c.name), None)
    # print(optional_container)

    # if optional_container == None:
    #     docker_client.images.pull('docker/whalesay')

    # if not optional_container:
    #     print('Creating container whalesay-py . . .')
    #     created_container = docker_client.containers.create('docker/whalesay',
    #                                                         command=['cowsay', 'hello there'],
    #                                                         name='whalesay-py')
    #     created_container.start()
    #     print('Container created and started')
    #     optional_container = created_container

    # log_output = optional_container.logs(stream=True,
    #                                      stderr=True,
    #                                      stdout=True,
    #                                      timestamps=False,
    #                                      tail='all')
    # for log in log_output:
    #     log_line = log.decode().rstrip()
    #     print(log_line)

    # print('\nCreating a command-result dictionary of multiple containers')
    # commands = []
    # commands.append(('cowsay', 'monday'))
    # commands.append(('cowsay', 'tuesday'))
    # commands.append(('cowsay', 'wednesday'))
    # command_result = {}

    # for command_to_run in commands:
    #     print(f'\nCreating container of command {command_to_run} . . .')
    #     command_container = docker_client.containers.create('docker/whalesay',
    #                                                         command=command_to_run,
    #                                                         name='command-container')
    #     command_container.start()
    #     command_container_output = command_container.logs(stream=True,
    #                                                       stderr=True,
    #                                                       stdout=True,
    #                                                       timestamps=False,
    #                                                       tail='all')
    #     log_lines = []
    #     for log in command_container_output:
    #         log_line = log.decode().rstrip()
    #         log_lines.append(log_line)
    #     command_result[command_to_run] = '\n'.join(log_lines)
    #     command_container.stop()
    #     command_container.remove()
    #     print('Deleted container of command ', command_to_run)

    # print('\nKey-value pair of the command-result dictionary:')
    # for key, value in command_result.items():
    #     print(f'\nKey: {type(key)} {key}')
    #     print(f'Value: {type(value)}\n {value}')

    docker_client.images.pull('eclipse-temurin:17')

    try:
        temurin_git_image = docker_client.images.get('eclipse-temurin-git:17')
    except:      
        with open('.Dockerfile', 'w') as file:
            file.write('FROM eclipse-temurin:17\nRUN apt-get update && apt-get install -y git')

        temurin_git_image, build_logs = docker_client.images.build(
            path=r'.',
            dockerfile='.Dockerfile',
            tag='eclipse-temurin-git:17',
            rm=True
        )

        if os.path.exists('./.Dockerfile'):
            os.remove('./.Dockerfile')

    container_list = docker_client.containers.list(all=True)

    for container in container_list:
        if container.name == "eclipse-temurin-git":
            temurin_git_container = docker_client.containers.get('eclipse-temurin-git')
            break
    else:
        temurin_git_container = docker_client.containers.create(
            image=temurin_git_image,
            name='eclipse-temurin-git',
            detach=True,
            working_dir='/app'
        )

    # Running the container
    temurin_git_container.start()

    exec_result = temurin_git_container.exec_run('git init')
    output = exec_result.output.decode('utf-8')
    print(output)

    exec_result = temurin_git_container.exec_run('git status')
    output = exec_result.output.decode('utf-8')
    print(output)


if __name__ == '__main__':
    main()
