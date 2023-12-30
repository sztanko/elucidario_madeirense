import AboutProjectEn from './AboutProjectEn'
import AboutProjectPt from './AboutProjectPt'
import AboutProjectUk from './AboutProjectUk'
import AboutProjectDe from './AboutProjectDe'
import AboutProjectRu from './AboutProjectRu'


export const AboutProject = ({locale}) => {
    if (locale === 'en')
        return <AboutProjectEn />
    if (locale === 'pt')
        return <AboutProjectPt />
    if (locale === 'de')
        return <AboutProjectDe />
    if (locale === 'ru')
        return <AboutProjectRu />
    if (locale === 'uk')
        return <AboutProjectUk />
    return <AboutProjectEn />
}