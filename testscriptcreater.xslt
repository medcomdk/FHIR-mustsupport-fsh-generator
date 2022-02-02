<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
    xmlns:f="http://hl7.org/fhir" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">  
    <xsl:template match="/">
        <html>
            <body>
                <h2>SUSHI Mustsupport test Ruleset </h2>
                <table border="1">
                    <tr bgcolor="#9acd32">
                        <th>FHIRPath</th>
                    </tr>
                    <xsl:for-each select="f:StructureDefinition/f:snapshot/f:element">
                        <xsl:if test="f:mustSupport/@value ='true'">
                            <tr>
                                <td>
                                    RuleSet: testMustSupport<xsl:value-of select="translate(f:path/@value,'.','')"/><br/>
                                    * test[=].action[+].assert.description = "Mustsupport test for <xsl:value-of select="f:path/@value"/>"<br/>
                                    * test[=].action[=].assert.direction = #request<br/>
                                    * test[=].action[=].assert.expression = 
                                    "Bundle.entry.resource.ofType(<xsl:value-of select="substring-before(f:path/@value,'.')"/>).<xsl:value-of select="translate(substring-after(f:path/@value,'.'),'[x]','')"/>.exists()"<br/>
                                    * test[=].action[=].assert.warningOnly = true<br/>                                   
                                    <br/>
                                </td>  
                                
                            </tr> 
                        </xsl:if>
                    </xsl:for-each>
                </table>
            </body>
        </html>
    </xsl:template>   
</xsl:stylesheet>