## Pixiv����

- ����ȷ��������������Pվ������
- ����ȷ��������������Pվ������
- ����ȷ��������������Pվ������

##### ��ҪPython3.6�����ϲ�����������

����һ�����̵߳�Pվ���棬û������̣߳�������ȡ�ٶ��е���������ʹ��Ӧ��û�����⡣
����û����`sleep`���벻Ҫ��ʱ������ȡ�����������ʱban��ip��

��¼����ڴ��ļ�Ŀ¼������cookie�ļ����벻Ҫ�޸Ļ�ɾ�����ļ�������ᵼ��cookie��ϢʧЧ��Ҳ��Ҫ�������ˣ���ʹ�ʺ���Ϣй¶��

����ʹ����`requests , BeautifulSoup , lxml`����������������У������Ƿ�װ����ĵ������⡣

�������ص㣺
1. ֧��ָ����ȡ����
2. ֧��ָ����ȡ��
3. ֧��ָ����ȡҳ��
4. ���غ��ͼƬ�����ļ��з��࣬�ļ�����PվID����

����֮����
1. û�м�����̹߳���
2. û���������������������Ż�
3. û�б��ػ��洢δ��ȡ���ӣ����������������






## Pixiv Spider

- Please confirm your network can open pixiv first!!!
- Please confirm your network can open pixiv first!!!
- Please confirm your network can open pixiv first!!!

##### Require Python3.6 and above to run normally

This is a single-threaded spider,so the speed not fast,personal use should be ok.
Please don't crawling frequent in short time,it will ban your ip temporary.

When logined in it will have a cookie file,don't modity or delete this file and don't send this file to other people.

Before use please install`requests , BeautifulSoup , lxml`.

Feature:
1. can set crawling date
2. can set crawling list
3. can set crawling page
4. downloaded picture sort by list type,filename is picture id

Shortcoming:
1. no multiprocess function
2. no optimization for network connectivity issues
3. no localised storage for uncrawled links (reducing server load) 