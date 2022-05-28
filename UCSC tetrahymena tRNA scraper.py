from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time


driver = webdriver.Chrome('./chromedriver')

# Add the genes you want to scrape to this genes.txt file
with open('genes.txt') as f:
    genes = f.readlines()

genes = [x.strip() for x in genes] 

# Define the columns you want to scrape
gene_list = []
region_list = []
gensize_list = []
strand_list = []
sequence_list_b = []
sequence_list_a = []
sequence_list_rev_a = []
sequence_list_rev_b = []

# Begin the scraping process
driver.get("https://genome.ucsc.edu/cgi-bin/hgHubConnect?hubUrl=https%3A%2F%2Fdatahub-470-p17.p.genap.ca%2Fhub.txt&hgHub_do_firstDb=on&hgHub_do_redirect=on&hgHubConnect.remakeTrackHub=on&hgsid=1190106735_96ex38OZANHTAaLlgKF9VKc4ku0b")
time.sleep(1)

for gene in genes:

    gene_list.append(gene)
    driver.get("https://genome.ucsc.edu/cgi-bin/hgTracks?db=hub_2893147_T_thermophila&lastVirtModeType=default&lastVirtModeExtraState=&virtModeType=default&virtMode=0&nonVirtPosition=&position=chr_135%3A1099873%2D1099945&hgsid=1131674227_Tnhf8Xh3rObUyIZH5U57VqKjXHzy")
    driver.find_element_by_xpath("/html/body/form[2]/center/input[3]").send_keys(gene)
    driver.find_element_by_xpath('/html/body/form[2]/center/input[4]').click()

    time.sleep(1)

    region = driver.find_element_by_xpath('/html/body/form[2]/center/span[1]').text
    region_list.append(region)
    chr = region.split(':')[0]
    begin_region = region.replace(chr + ':','').replace(',','').split('-')[0]
    end_region =   region.replace(chr + ':','').replace(',','').split('-')[1]

    print(gene, chr, begin_region, end_region)
    
    # next url
    next_url = "https://genome.ucsc.edu/cgi-bin/hgc?hgsid=1131674227_Tnhf8Xh3rObUyIZH5U57VqKjXHzy&db=hub_2893147_T_thermophila&c="+ chr +"&l=" + str(int(begin_region) - 1) + "&r=" + end_region + "&o=" + str(int(begin_region) - 1) + "&t=" + end_region + "&g=hub_2893147_Annotation&i=" + gene + ".t1"
    driver.get(next_url)
    
    time.sleep(1)

    full_text = driver.find_element_by_xpath('/html/body/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td[2]').text

    gensize_i = full_text.find('Genomic Size: ')
    strand_i = full_text.find('Strand: ')

    gen_size = full_text[gensize_i + 14 : gensize_i + 17]
    strand = full_text[strand_i + 8 : strand_i + 10]

    gensize_list.append(gen_size)
    strand_list.append(strand)

    # sequences
    driver.find_element_by_xpath('/html/body/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td[2]/a[2]').click()
    time.sleep(1)

    driver.find_element_by_id("hgSeq.padding5").clear()
    driver.find_element_by_id("hgSeq.padding3").clear()
    driver.find_element_by_id("hgSeq.padding5").send_keys('500')
    driver.find_element_by_id("hgSeq.padding3").send_keys('250')


    box = driver.find_element_by_xpath('/html/body/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td[2]/form/input[18]')
    
    if box.is_selected() == True:

        box.click()

    driver.find_element_by_xpath('//*[@id="submit"]').click()

    time.sleep(1)
    sequence = driver.find_element_by_xpath('/html/body/pre').text
    
    try:
        sequence_list_a.append(sequence.split("none")[0]+"none")
    except:
        sequence_list_a.append("")
    try:
        sequence_list_b.append(' '.join(sequence.split("none")[1].split()))
    except:
        sequence_list_b.append("")


    driver.get(next_url)
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td[2]/a[2]').click()
    time.sleep(1)
    box = driver.find_element_by_xpath('/html/body/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td[2]/form/input[18]')
    
    if box.is_selected() == False:
        box.click()

    driver.find_element_by_xpath('//*[@id="submit"]').click()

    time.sleep(1)
    sequence = driver.find_element_by_xpath('/html/body/pre').text
    
    try:
        sequence_list_rev_a.append(sequence.split("none")[0]+"none")
    except:
        sequence_list_rev_a.append("")
    try:
        sequence_list_rev_b.append(' '.join(sequence.split("none")[1].split()))
    except:
        sequence_list_rev_b.append("")

    
        
time.sleep(1)
driver.close()

# Save the scraped data to a dataframe
df = pd.DataFrame()
df['Gene'] = gene_list
df['region_list'] = region_list
df['gensize_list'] = gensize_list
df['strand_list'] = strand_list
df['sequence_list_a'] = sequence_list_a
df['sequence_list_b'] = sequence_list_b

df['sequence_list_rev_a'] = sequence_list_rev_a
df['sequence_list_rev_b'] = sequence_list_rev_b


# Change the name of the excel file here
df.to_excel('tRNA Seqalt.xlsx')
