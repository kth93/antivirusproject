import k2rc4

if __name__ == '__main__':
    rc4 = k2rc4.RC4()
    rc4.set_key('PASSWORD1234')
    crypt_Text = rc4.crypt('hello')

    rc4 = k2rc4.RC4()
    rc4.set_key('PASSWORD1234')
    decrypt_Text = rc4.crypt(crypt_Text)
    print(decrypt_Text)