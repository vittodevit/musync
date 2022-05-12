import click


@click.command()
@click.argument('configfile')
def main(configfile):
    try:
        f = open(configfile, "r")
        click.echo(f.read())
    except:
        click.echo("File di configurazione illegibile")


if __name__ == '__main__':
    main()
