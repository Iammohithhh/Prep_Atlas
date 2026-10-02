def convert_to_ipv6(ipv4):
    octets = list(map(int, ipv4.split('.')))
    if octets[0] == 127:                                # loopback
        return '::1'
    hexed = ['%02X' % o for o in octets]
    return '::FFFF:' + hexed[0] + hexed[1] + ':' + hexed[2] + hexed[3]

# ---- tests
assert convert_to_ipv6('192.168.10.92') == '::FFFF:C0A8:0A5C'
assert convert_to_ipv6('127.0.0.1') == '::1'
assert convert_to_ipv6('0.0.0.0') == '::FFFF:0000:0000'
assert convert_to_ipv6('255.255.255.255') == '::FFFF:FFFF:FFFF'
print('ok')
