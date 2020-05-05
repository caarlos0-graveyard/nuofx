# nuofx

Export NuBank's _NuConta_ statements as an OFX file.

## Usage

Easiest way is using Docker:

```sh
docker run --rm -it -e NU_CPF=xxxxx -e NU_PWD=xxxxx -v $PWD:/tmp caarlos0/nuofx
```

> `NU_CPF` should be your CPF, numbers only
> `NU_PWD` should be your NuBank password

It should display a QR Code. With your phone, open the NuBank app, go to
"Perfil" > "Acesso pelo site", scan it, and then press enter on the terminal window.

It should generate a `extrato_nuconta.ofx` file on your current directory, 
which you can import on any software that can speaks OFX.
