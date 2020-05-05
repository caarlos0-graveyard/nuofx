# nuofx

Export NuBank's _NuConta_ statements as an OFX file.

```sh
docker run --rm -e NU_CPF=xxxxx -e NU_PWD=xxxxx -v $PWD:/tmp caarlos0/nuofx
```

It should display a QR Code. With your phone, open the NuBank app, go to
"Perfil" > "Acesso pelo site", scan it, and then press enter on the terminal window.

It should generate a `/tmp/extrato_nuconta.ofx` file that you can import on anything that
can speaks OFX.
