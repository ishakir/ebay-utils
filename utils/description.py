from bs4 import BeautifulSoup, Comment

border = '''
<table cellpadding="0" cellspacing="28" width="100%">
 <tbody>
  <tr>
   <td valign="top">
    <table border="0" cellpadding="0" cellspacing="0" width="100%">
     <tbody>
      <tr>
       <td>
        <div align="center">
         <table bgcolor="#000000" border="0" cellpadding="0" cellspacing="0" width="900">
          <tbody>
           <tr>
            <td valign="top">
             <table border="0" cellpadding="0" cellspacing="1" width="100%">
              <tbody>
               <tr>
                <td bgcolor="#ffffff" valign="top">
                 <table border="0" cellpadding="0" cellspacing="0" width="100%">
                  <tbody>
                   <tr>
                    <td valign="top">
                     <img border="0" height="252" src="http://freeauctiondesigns.com/ebay/templates/green_white_swirls/top.gif" width="900"/>
                    </td>
                   </tr>
                   <tr>
                    <td valign="top">
                     <table border="0" cellpadding="5" cellspacing="5" width="100%">
                      <tbody>
                       <tr>
                        <td valign="top">
                         <center>
                          <div class="bodycolumn" id="templatebody">
                           <div class="tempwidget" id="templatetitle">
                            <div class="temp-content">
                             <center>
                             	{}
                             </center>
                            </div>
                           </div>
                           <div class="tempwidget" id="templatefoot">
                            <div class="temp-content">
                             <center>
                              <p align="center" class="MsoNormal" style="TEXT-ALIGN: center; MARGIN: 0cm 0cm 0pt; mso-pagination: widow-orphan; mso-margin-top-alt: auto; mso-margin-bottom-alt: auto">
                               <br/>
                              </p>
                             </center>
                            </div>
                           </div>
                          </div>
                         </center>
                        </td>
                       </tr>
                       <tr>
                        <td valign="top">
                        </td>
                       </tr>
                      </tbody>
                     </table>
                    </td>
                   </tr>
                  </tbody>
                 </table>
                </td>
               </tr>
              </tbody>
             </table>
            </td>
           </tr>
          </tbody>
         </table>
        </div>
        <div align="center">
        </div>
       </td>
      </tr>
     </tbody>
    </table>
   </td>
  </tr>
 </tbody>
</table>
'''

def fix_description(description):
	soup = BeautifulSoup(description, 'html.parser')
	match = soup.findAll('script')
	if match:
		for m in match:
			m.decompose()

	match2 = soup.findAll('o:p')
	if match2:
		for m in match2:
			m.decompose()

	comments = soup.findAll(text=lambda text: isinstance(text, Comment))
	[comment.extract() for comment in comments]

	if soup.find('img', {'src': 'http://freeauctiondesigns.com/ebay/templates/green_white_swirls/top.gif'}):
		return soup.encode_contents(formatter='html').decode('utf-8')
	else:
		return BeautifulSoup(border.format(soup.encode_contents(formatter='html')), 'html.parser').encode_contents(formatter='html').decode('utf-8')
