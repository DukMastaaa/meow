thingy = '1962\n1577\n1750\n1836\n1762\n1691\n1726\n1588\n1370\n1043\n1307\n1552\n1813\n1804\n1765\n1893\n1610\n764\n1512\n1404\n1711\n1000\n1694\n1546\n1880\n1721\n2006\n1787\n1510\n1850\n1420\n1712\n1926\n1707\n1983\n1680\n1436\n389\n1448\n1875\n1333\n1733\n1935\n1794\n1337\n1863\n1769\n1635\n1499\n1807\n1326\n1989\n1705\n1673\n1829\n1684\n1716\n456\n1696\n1398\n1942\n1851\n1690\n1328\n1356\n1775\n1564\n1466\n1273\n1896\n766\n1814\n1810\n1537\n1463\n1755\n1341\n1665\n1520\n1366\n1387\n1976\n1717\n1737\n1551\n1760\n1496\n1664\n1450\n1319\n1674\n1630\n1301\n1330\n1658\n1637\n1655\n1439\n1832\n1948\n1339\n1656\n1449\n1296\n1489\n1758\n1939\n1857\n1402\n1394\n1882\n1446\n1412\n1430\n1212\n1377\n1501\n1873\n1812\n1667\n1560\n1654\n1575\n1999\n1581\n1792\n1299\n1843\n1383\n1351\n1297\n1822\n1801\n1977\n1316\n1477\n1980\n1693\n1220\n1554\n1607\n1903\n1669\n1593\n1955\n1286\n1909\n1280\n1854\n2005\n1820\n1803\n1763\n1660\n1410\n1974\n1808\n1816\n1723\n1936\n1423\n1818\n1800\n1294\n857\n496\n1248\n1670\n1993\n1929\n1966\n1381\n1259\n1285\n1797\n1644\n1919\n1267\n1509\n399\n1300\n1662\n1556\n1747\n1517\n1972\n1729\n1506\n1544\n1957\n1930\n1956\n1753\n1284\n1389\n1689\n1709\n1627\n1770\n847'
numbers = [int(num) for num in thingy.split("\n")]
# i mean it works

TARGET = 2020

def part_a():
    odd = sorted([num for num in numbers if num % 2 == 1])
    even = sorted([num for num in numbers if num % 2 == 0])
    for parity in odd, even:
        parity_len = len(parity)
        for end_index in range(1, parity_len + 1):
            diff = TARGET - parity[-end_index]
            for pair_index in range(parity_len - end_index):
                if parity[pair_index] == diff:
                    # we found a match!
                    first_num = parity[-end_index]
                    second_num = parity[pair_index]
                    assert first_num + second_num == TARGET
                    return first_num * second_num
    # pog


def part_b():
    # uhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh not efficient at all but sure
    number_len = len(numbers)
    for end_index in range(1, number_len + 1):
        end_num = numbers[-end_index]
        for middle_index in range(end_index, number_len + 1):  # probably a bug here
            middle_num = numbers[-middle_index]
            for start_index in range(middle_index):
                start_num = numbers[start_index]
                total = start_num + middle_num + end_num
                if total == TARGET:
                    return start_num * middle_num * end_num
    return "it doesn't work"


PARITIES = {  # true indicates odd
    (True, True): False,
    (True, False): True,
    (False, True): True,
    (False, False): False
}


def better_part_b():
    # going to adapt part_b with some strategy from part_a
    number_len = len(numbers)
    triplet = [False, False]
    for end_index in range(1, number_len + 1):
        end_num = numbers[-end_index]
        triplet[0] = end_num % 2 == 1
        for middle_index in range(end_index, number_len + 1):  # probably a bug here
            middle_num = numbers[-middle_index]
            triplet[1] = middle_num % 2 == 1
            for start_index in range(middle_index):
                start_num = numbers[start_index]
                if PARITIES[tuple(triplet)] == (start_num % 2 == 1):  # ignore the TypeError
                    total = start_num + middle_num + end_num
                    if total == TARGET:
                        return start_num * middle_num * end_num


if __name__ == '__main__':
    print(better_part_b())
    print(part_b())