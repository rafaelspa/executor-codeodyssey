import docker
import os

def main():
    global temurin_gradlew_container
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

    # docker_client.images.pull('eclipse-temurin:17')

    project_name = "gradlew-project"
    image_tag_name = "temurin-gradlew:17"
    container_name = "temurin_gradlew"

    # Create Dockerfile, overwriting preexistent
    with open('.Dockerfile', 'w') as file:
        file.write(
            '''
            FROM eclipse-temurin:17\n
            RUN apt-get update\n
            RUN mkdir /app\n
            COPY {project_name} /app/{project_name}\n
            WORKDIR /app\n
            CMD ["./gradlew", "test"]
        '''.format(project_name=project_name)
        )

    # build an image from the Dockerfile
    temurin_gradlew_image, build_logs = docker_client.images.build(
        path=r'.',
        dockerfile='.Dockerfile',
        tag=image_tag_name,
        rm=True
    )

    # delete the Dockerfile
    if os.path.exists('./.Dockerfile'):
        os.remove('./.Dockerfile')

    # Create a container from the image
    temurin_gradlew_container = docker_client.containers.create(
        image=temurin_gradlew_image,
        name=container_name,
        working_dir=f'/app/{project_name}'.format(project_name=project_name)
    )

    # Start the container
    temurin_gradlew_container.start()

    # Create logs
    logs = temurin_gradlew_container.logs(
        stream=True,
        stderr=True,
        stdout=True,
        timestamps=False,
        tail='all'
    )

    log_lines = []
    for log in logs:
        log_line = log.decode().rstrip()
        print(log_line)

    temurin_gradlew_container.stop()
    temurin_gradlew_container.remove()



    # exec_result_git_clone = temurin_gradlew_container.exec_run(
    #     cmd='git clone https://github.com/rafaelspa/hello-test-springboot.git'
    # )
    # output = exec_result_git_clone.output.decode('utf-8')
    # print(output)

    # print(temurin_gradlew_container.exec_run(
    #     cmd='cd'
    # ).output.decode('utf-8'))

    # temurin_gradlew_container.exec_run(
    #     cmd='chmod +x ./hello-test-springboot/gradlew'
    # )

    # exec_result_gradlewrun = temurin_gradlew_container.exec_run(
    #     cmd='./hello-test-springboot/gradlew bootRun'
    # )
    # print(exec_result_gradlewrun)
    # output = exec_result_gradlewrun.output.decode('utf-8')
    # print(output)

    # # The previous exec_run command stops the container
    # temurin_gradlew_container.restart()

    # exec_result_ls = temurin_gradlew_container.exec_run(
    #     cmd='ls -la ./hello-test-springboot'
    # )
    # output = exec_result_ls.output.decode('utf-8')
    # print(output)

    # temurin_gradlew_container.stop()

    # # docker_client.containers.prune()
    # docker_client.images.prune()


if __name__ == '__main__':
    main()
